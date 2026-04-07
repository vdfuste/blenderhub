import json
import os
import shutil
import tempfile
import webview

import src.blender as blender
import src.utils as utils
from src.locations import APP_DIR_NAME, INSTALLS_DIR, LOCAL_APP_DATA, OS_PLATFORM, RELEASES_DATA

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
			app_name:str = "blender"
			if OS_PLATFORM == "windows":
				app_name = "blender.exe"

			version:str = folder.split("-", 2)[1]
			self.installed.append(version)
			self.executes[version] = os.path.join(INSTALLS_DIR, folder, app_name)

	def __get_releases(self) -> None:
		data:dict = utils.download_releases_data()
		
		if not os.path.isdir(LOCAL_APP_DATA):
			os.makedirs(LOCAL_APP_DATA)
		
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
		
	# INSTALLED VERSIONS
	def open_project(self, data:dict) -> None:
		# TODO: Move this method to projects.py

		exec_path:str = self.executes[data["version"]]
		filepath:str = data["filepath"]
		utils.execute([exec_path, filepath], no_parent=True)
	
	def open_version(self, version:str=None) -> None:
		version = version or self.installed[-1]
		utils.execute(self.executes[version], no_parent=True)
	
	def create_project(self, data:dict) -> bool:
		# TODO: Move this method to projects.py

		filename, path, version = data.values()
		filename = f"{filename}.blend"
		filepath:str = os.path.join(path, filename)
		
		if os.path.isfile(filepath):
			print(f"{filename} already exists in {path}!")
			return False

		exec_path:str = self.executes[version]
		blender.create_project(exec_path, filepath)
		
		return True

	# INSTALL AND UNINSTALL VERSIONS
	def __download_version(self, checksum, filename):		
		# blender-x.y.z-platform-architecture.tar.xz -> ["blender", "x.y.z", "platform", "architecture.tar.xz"]
		_, version, platform, arch_ext = filename.split("-")
		major, minor, _ = version.split(".")
		architecture, extension = arch_ext.split(".", 1)
		extension = f".{extension}"

		# Creating a temporal folder.
		temp_folder:str = tempfile.gettempdir()
		temp_folder = os.path.join(temp_folder, APP_DIR_NAME)
		temp_filename:str = os.path.join(temp_folder, filename)

		os.makedirs(temp_folder, exist_ok=True)

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
				
				self.install_process = utils.execute(
					["curl", "--progress-bar", "-o", temp_filename, f"{URL}{folder_version}{filename}"],
					no_parent=True,
					text=True
				)

				for line in self.install_process.stderr:					
					download_output:list = line.strip().split()
					if len(download_output) == 2:
						percent = download_output[1]
						if "%" in percent:
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
					return ("error", "Invalid or corrupted installer", ":(")
			
			folder_name:str = filename.replace(extension, "")
			return (temp_folder, folder_name, filename)
		
		except Exception as e:
			return ("error", e, ":O")
	
	def install_version(self, version:str, passw:str) -> None:		
		temp_folder, folder_name, filename = self.__download_version(**self.releases[version])
		temp_filename:str = os.path.join(temp_folder, filename)
		temp_folder_name:str = os.path.join(temp_folder, folder_name)
		install_folder_name:str = os.path.join(INSTALLS_DIR, folder_name)

		# TODO: Find a better way to check errors.
		if temp_folder == "error":
			print(temp_folder_name, temp_filename)

			webview.windows[0].state.install_process = {
				"percent": 0,
				"feedback": f"Error installing Blender {version}"
			}
			return
		
		try:
			# Extracting files.
			webview.windows[0].state.install_process = {
				"percent": percents["EXTRACTING"] * 100,
				"feedback": "Extracting files"
			}

			print("\nExtracting files")
			print(temp_filename, " in ", temp_folder)
			
			# TODO: Track the process on the loading bar.
			#self.install_process = 
			utils.execute(["tar", "-xf", temp_filename, "-C", temp_folder])

			# Moving extracted folder from temporal folder to blenderhub folder.
			webview.windows[0].state.install_process = {
				"percent": percents["MOVING"] * 100,
				"feedback": f"Installing Blender {version}"
			}
			
			if OS_PLATFORM == "linux":
				utils.execute(["sudo", "mkdir", "-p", INSTALLS_DIR])
				utils.execute(["sudo", "mv", temp_folder_name, INSTALLS_DIR])
			elif OS_PLATFORM == "windows":
				os.makedirs(INSTALLS_DIR, exist_ok=True)
				os.rename(temp_folder_name, install_folder_name)

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
	
	def remove_version(self, version:str, passw:str) -> None:
		remove_dirname:str = os.path.dirname(self.executes[version])
		remove_dirname = os.path.join(INSTALLS_DIR, remove_dirname)

		print(remove_dirname)
		
		webview.windows[0].state.remove_process = {
			"percent": 5,
			"feedback": f"Removing Blender {version}"
		}
		
		try:
			if OS_PLATFORM == "linux":
				utils.execute(["sudo", "rm", "-rf", remove_dirname])
			elif OS_PLATFORM == "windows":
				shutil.rmtree(remove_dirname)
		
			webview.windows[0].state.remove_process = {
				"percent": 100,
				"feedback": f"Blender {version} removed successfully!"
			}

			self.__get_installed_versions()
			self.__get_releases()
		
		except Exception as e:
			webview.windows[0].state.remove_process = {
				"percent": 0,
				"feedback": f"An error ocurred while removing Blender {version}!"
			}
			print(e)
