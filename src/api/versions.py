import json
import os
import subprocess
import tempfile
import webview

import src.utils as utils
from src.locations import INSTALLS_DIR, OS_PLATFORM, RELEASES_DATA

percents:dict = {
	"INIT": 0.05,		 #   5%
	"DOWNLOADING": 0.75, #  75%
	"EXTRACTING": 0.85,	 #  85%
	"MOVING": 0.95,		 #  95%
	"DONE": 1			 # 100%
}

class Versions:
	def __init__(self):
		self.install_process = None

		self.__get_installed_versions()
		self.__get_releases()

	def __get_installed_versions(self) -> None:
		self.installed:list = []
		self.executes:dict = {}

		if not os.path.isdir(INSTALLS_DIR):
			return

		folders:list = os.listdir(INSTALLS_DIR)
		folders.sort()

		for folder in reversed(folders):
			if OS_PLATFORM == "linux":
				version:str = folder.split("-", 2)[1]
				self.installed.append(version)
				self.executes[version] = os.path.join(INSTALLS_DIR, folder, "blender")
			
			#elif OS_PLATFORM == "macos":
			#	pass
			
			elif OS_PLATFORM == "windows":
				version:str = folder.split(" ")[1]
				self.installed.append(version)
				self.executes[version] = os.path.join(INSTALLS_DIR, folder, "blender.exe")

	def __get_releases(self) -> None:
		data:dict = utils.download_releases_data()
		
		with open(RELEASES_DATA, "w") as file:
			json.dump(data, file)
		
		self.releases:dict = {}
		self.releases_ui:dict = {
			# TODO: Generate series lists based on the stored/downloaded data.
			"series": {
				"serie-5": [],
				"serie-4": [],
				"serie-3": [],
				"LTS": []
			},
			"allVersions": []
		}
		
		index:int = 0
		for serie, versions in reversed(data.items()):
			for version, value in reversed(versions.items()):
				subversions:list = [key for key in value["subversions"]]
				installed:list = [sub for sub in reversed(subversions) if sub in self.installed]
				available:list = [sub for sub in reversed(subversions) if sub not in installed]

				_version:dict = {
					"version": version,
					"subversions": [
						{
							"title": "Available Versions",
							"items": available
						},
						{
							"title": "Installed Versions",
							"items": installed
						},
					],
					"urlImage": value["url_image"]
				}

				if "lts" in value:
					_version.update({ "lts": True })
					self.releases_ui["series"]["LTS"].append(index)
				
				self.releases.update(value["subversions"])
				self.releases_ui["allVersions"].append(_version)
				self.releases_ui["series"][serie].append(index)

				index += 1
	
	def __exec(self, commands, *, no_parent=False, stdout=None, stderr=None, **kwargs):
		try:
			func = subprocess.Popen if no_parent else subprocess.run
			return func(commands, stdout=stdout, stderr=stderr, **kwargs)
		except subprocess.CalledProcessError as e:
			print(f"Error executing commands: {e}")
	
	# INSTALLED VERSIONS
	def open_project(self, data:dict) -> None:
		self.__exec([self.executes[data["version"]], data["filepath"]], no_parent=True)
	
	def open_version(self, version:str=None) -> None:
		version = version or self.installed[-1]
		self.__exec(self.executes[version], no_parent=True)
	
	def create_project(self, data:dict) -> bool:
		filename, path, version = data.values()
		filename = f"{filename}.blend"
		filepath:str = os.path.join(path, filename)
		
		if os.path.isfile(filepath):
			print(f"{filename} already exists in {path}!")
			return False
		
		self.__exec([
			self.executes[version], "--background", "--python",
			"src/blender/create.py", filepath
		])
		
		return True

	# INSTALL AND UNINSTALL VERSIONS
	def __download_version(self, checksum, filename):		
		# blender-x.y.z-linux-x64.tar.xz -> ["blender", "x.y.z", "linux", "x64.tar.xz"]
		_, version, platform, arch_ext = filename.split("-")
		major, minor, _ = version.split(".")
		architecture, extension = arch_ext.split(".", 1)
		extension = f".{extension}"

		# Creating a temporal folder.
		temp_folder:str = tempfile.gettempdir()
		temp_filename:str = os.path.join(temp_folder, filename)

		# Updating the loading bar state.
		webview.windows[0].state.install_process = {
			"percent": 0,
			"feedback": "Initializing process"
		}

		# Checking if the file is already downloaded and is not corrupted.
		is_valid_installer:bool = False
		if os.path.isfile(temp_filename):
			checksum_installer:str = utils.generate_checksum(temp_filename)
			is_valid_installer = checksum == checksum_installer
		
		try:
			# Downloading the Blender installer on the temporal folder if is not already downloaded.
			if not is_valid_installer:
				URL:str = "https://download.blender.org/release/"
				folder_version:str = f"Blender{major}.{minor}/"
			
				current_percent:int = percents["INIT"] * 100
				webview.windows[0].state.install_process = {
					"percent": current_percent,
					"feedback": "Downloading files"
				}
				
				self.install_process = self.__exec(
					["curl", "--progress-bar", "-o", filename, f"{URL}{folder_version}{filename}"],
					no_parent=True,
					stderr=subprocess.PIPE,
					text=True
				)

				for line in self.install_process.stderr:					
					download_output:list = line.strip().split()
					if len(download_output) == 2:
						percent = download_output[1]
						percent = int(percent.split(".")[0])
						webview.windows[0].state.install_process = {
							"percent": percent * percents["DOWNLOADING"] + current_percent,
							"feedback": "Downloading files"
						}
			
				# Checking the downloaded file.
				checksum_installer = utils.generate_checksum(temp_filename)
				is_valid_installer = checksum == checksum_installer

				if not is_valid_installer:
					os.remove(temp_filename)
					return ("error", "Invalid or corrupted installer")
			
			temp_folder_name:str = temp_filename.replace(extension, "")
			return (temp_folder, temp_folder_name, temp_filename)
		
		except Exception as e:
			return ("error", e)
	
	def install_version_on_linux(self, version:str, passw:str) -> None:
		temp_folder, temp_folder_name, temp_filename = self.__download_version(**self.releases[version])

		if temp_folder_name == "error":
			webview.windows[0].state.install_process = {
				"percent": 0,
				"feedback": f"Error installing Blender {version}"
			}
			return
		
		try:
			# Extracting files from the .tar.xz file.
			webview.windows[0].state.install_process = {
				"percent": percents["EXTRACTING"] * 100,
				"feedback": "Extracting files"
			}

			self.install_process = self.__exec(["tar", "-xf", temp_filename, "-C", temp_folder])

			# Moving extracted folder from /tmp folder to /opt/blender folder.
			webview.windows[0].state.install_process = {
				"percent": percents["MOVING"] * 100,
				"feedback": f"Installing Blender {version}"
			}

			self.install_process = self.__exec(["sudo", "mkdir", "-p", INSTALLS_DIR])
			self.install_process = self.__exec(["sudo", "mv", temp_folder_name, INSTALLS_DIR])
			
			# Finish process.
			webview.windows[0].state.install_process = {
				"percent": 100,
				"feedback": f"Blender {version} successfully installed!"
			}

			self.__get_installed_versions()
			self.__get_releases()

		except Exception as e:
			webview.windows[0].state.install_process = {
				"percent": 0,
				"feedback": f"Error installing Blender {version}"
			}
			print(e)
	
	def install_version_on_window(self, version:str) -> None:
		# TODO: Check the CPU architecture (x64 or ARM).
		
		temp_folder, filename = self.__download_version(self.releases[version])
		temp_file:str = os.path.join(temp_folder, filename)
		print(temp_file)
		
		if not temp_file:
			print(f"Error installing Blender {version}")
			return
		
		# The installation will be managed by the .msix installer.
		webview.windows[0].state.install_process = {
			"percent": 100,
			"feedback": f"Opening Blender {version} installer"
		}
		
		# Running the .msix installer from PowerShell
		#self.install_process = 
		self.__exec(
			["msiexec", "/i", temp_file, "/norestart"],
			#no_parent=True,
			#stdout=subprocess.PIPE,
			#text=True
		)
	
	def remove_version_on_linux(self, version:str, passw:str) -> None:
		remove_process = self.__exec(
			["sudo", "rm", "-rf", f"{INSTALLS_DIR}/blender-{version}-linux-x64"],
			no_parent=True,
			stdout=subprocess.PIPE,
			text=True
		)

		for line in remove_process.stdout:
			percent:int = 25
			percent_bar:list = line.strip().split()
			
			if percent_bar[1]:
				percent = int(percent_bar[1].split(".")[0])
		
			webview.windows[0].state.remove_process = {
				"percent": percent,
				"feedback": f"Removing Blender {version}"
			}
		
		webview.windows[0].state.remove_process = {
			"percent": 100,
			"feedback": f"Blender {version} removed successfully!"
		}

		self.__get_installed_versions()
		self.__get_releases()

	def remove_version_on_windows(self, version:str) -> None:
		pass
