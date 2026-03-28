import json
import os
import subprocess
import tempfile
import webview

import src.utils as utils
from src.locations import INSTALLS_DIR, OS_PLATFORM, RELEASES_DATA

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
		data:dict = {}
		if os.path.isfile(RELEASES_DATA):
			with open(RELEASES_DATA, "r") as file:
				data = json.load(file)
		else:
			data = utils.download_releases_data()
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
	def __download_version(self, subversion:dict) -> str:
		URL:str = "https://download.blender.org/release/"

		checksum, filename = subversion.values()
		major, minor, _ = filename.split("-")[1].split(".")
		folder_version = f"Blender{major}.{minor}/"

		# Creating and moving to a temporal folder.
		temp_folder:str = tempfile.gettempdir()
		os.chdir(temp_folder)

		# Updating the loading bar state.
		webview.windows[0].state.install_process = {
			"percent": 5,
			"feedback": "Initializing process"
		}

		# Checking if the file is already downloaded and is not corrupted.
		is_valid_installer:bool = False
		if os.path.isfile(filename):
			checksum_installer:str = utils.generate_checksum(filename)
			is_valid_installer = checksum == checksum_installer
		
		# Downloading the Blender installer on the temporal folder if is not already downloaded.
		if not is_valid_installer:
			self.install_process = self.__exec(
				["curl", "--progress-bar", "-o", filename, f"{URL}{folder_version}{filename}"],
				no_parent=True,
				stderr=subprocess.PIPE,
				text=True
			)

			for line in self.install_process.stderr:
				percent:int = 5
				percent_bar:list = line.strip().split()
				
				if len(percent_bar) == 2:
					percent = int(percent_bar[1].split(".")[0])
				
				webview.windows[0].state.install_process = {
					"percent": percent,
					"feedback": "Downloading installer file"
				}
		
			# Checking the downloaded file.
			checksum_installer = utils.generate_checksum(filename)
			is_valid_installer = checksum == checksum_installer

			if not is_valid_installer:
				try:
					os.remove(filename)
				except Exception as e:
					print(f"Error trying to delete the installer on the temporal folder. {e}")
				
				return ""
		
		return os.path.join(temp_folder, filename)
	
	def install_version_on_linux(self, version:str, passw:str) -> None:
		temp_file:str = self.__download_version(version, self.releases[version])
		
		if not temp_file:
			print(f"Error installing Blender {version}")
			return
		
		# Extracting files from the .tar.xz file.
		self.install_process = self.__exec(
			["tar", "-xf", temp_file],
			no_parent=True,
			stdout=subprocess.PIPE,
			text=True
		)

		for line in self.install_process.stdout:
			percent:int = 85
			percent_bar:list = line.strip().split()
			
			if percent_bar[1]:
				percent = int(percent_bar[1].split(".")[0])
			
			webview.windows[0].state.install_process = {
				"percent": percent,
				"feedback": "Extracting files"
			}

		# Moving files from /tmp folder to /opt/blender folder.
		webview.windows[0].state.install_process = {
			"percent": 90,
			"feedback": f"Installing Blender {version}"
		}

		extracted_folder_name:str = self.releases[version]["filename"].split(".", 2)[0]
		self.install_process = self.__exec(["sudo", "mv", extracted_folder_name, INSTALLS_DIR])
		
		# Finish process.
		self.__get_installed_versions()
		webview.windows[0].state.install_process = {
			"percent": 100,
			"feedback": f"Blender {version} successfully installed!"
		}
	
	def install_version_on_window(self, version:str) -> None:
		# TODO: Check the CPU architecture (x64 or ARM).
		
		temp_file:str = self.__download_version(self.releases[version])
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
		
		self.__get_installed_versions()
		webview.windows[0].state.remove_process = {
			"percent": 100,
			"feedback": f"Blender {version} removed successfully!"
		}

	def remove_version_on_windows(self, version:str) -> None:
		pass
