import json
import os
import subprocess
import tempfile

import src.utils as utils
from src.locations import OPT_DIR, RELEASES_DATA

class Versions:
	def __init__(self):
		self.window = None
		self.install_process = None

		self.__get_installed_versions()
		self.__get_releases()

	def __get_installed_versions(self) -> None:
		self.installed:list = []
		self.executes:dict = {}

		folders:list = os.listdir(OPT_DIR)
		folders.sort()

		for folder in reversed(folders):
			version:str = folder.split("-", 2)[1]
			
			self.installed.append(version)
			self.executes[version] = os.path.join(OPT_DIR, folder, "blender")

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
				installed:list = [sub for sub in subversions if sub in self.installed]
				available:list = [sub for sub in subversions if sub not in installed]

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
	
	def set_window(self, window) -> None:
		self.window = window
	
	# INSTALLED VERSIONS
	def open_project(self, data:dict) -> None:
		self.__exec([self.executes[data["version"]], data["filepath"]], no_parent=True)
	
	def open_version(self, version:str=None) -> None:
		version = version or self.installed[-1]
		self.__exec(self.executes[version], no_parent=True)
	
	def create_project(self, data:dict) -> bool:
		filepath:str = os.path.join(data["path"], f"{data["filename"]}.blend")
		
		if os.path.isfile(filepath):
			print(f"{data["filename"]}.blend already exists in {data["path"]}!")
			return False
		else:
			script:str = f"import bpy; bpy.ops.wm.save_as_mainfile(filepath=\"{filepath}\")"
			commands:list = [self.executes[data["version"]], "--background", "--python-expr", script]
			self.__exec(commands)
			return True

	# INSTALL AND UNINSTALL VERSIONS
	def __download_version(self, version:str, passw:str, installer:str) -> str:
		# Creating and moving to a temporal folder.
		temp_folder:str = tempfile.gettempdir()
		os.chdir(temp_folder)

		major, minor, _ = version.split(".")
		folder_version:str = f"Blender{major}.{minor}"
		installer = f"blender-{version}-{installer}"

		# Checking if the file is already downloaded and is not corrupted.
		self.window.state.install_process = {
			"percent": 5,
			"feedback": "Initializing process"
		}

		is_valid_installer:bool = False
		
		if os.path.isfile(installer):
			checksum_installer:str = utils.generate_checksum(installer)
			is_valid_installer = checksum == checksum_installer
		
		# Downloading the Blender installer on the temporal folder.
		if not is_valid_installer:
			self.install_process = self.__exec([
				"curl", "--progress-bar", "-o", installer,
				f"https://download.blender.org/release/{folder_version}/{installer}"
			],
			no_parent=True,
			stderr=subprocess.PIPE,
			text=True)

			for line in self.install_process.stderr:
				percent:int = 50
				percent_bar:list = line.strip().split()
				
				if percent_bar[1]:
					percent = int(percent_bar[1].split(".")[0])
					print(percent)
				
				self.window.state.install_process = {
					"percent": percent,
					"feedback": "Downloading installer file"
				}
		
			# Checking the downloaded file.
			checksum_installer = utils.generate_checksum(installer)
			is_valid_installer = checksum == checksum_installer

			if not is_valid_installer:
				return ""
		
		return os.path.join(temp_folder, installer)
	
	def install_version_on_linux(self, version:str, passw:str) -> None:
		platform:str = "linux-x64"
		extension:str = ".tar.xz"
		temp_file:str = self.__download_version(version, passw, f"{platform}{extension}")
		
		if not temp_file:
			print(f"Error installing Blender {version}")
			return
		
		# Extracting files from the .tar.xz file.
		self.install_process = self.__exec(["tar", "-xf", temp_file],
		no_parent=True,
		stdout=subprocess.PIPE,
		text=True)

		for line in self.install_process.stdout:
			percent:int = 85
			percent_bar:list = line.strip().split()
			
			if percent_bar[1]:
				percent = int(percent_bar[1].split(".")[0])
			
			self.window.state.install_process = {
				"percent": percent,
				"feedback": "Extracting files"
			}

		# Moving files from /tmp folder to /opt/blender folder.
		self.window.state.install_process = {
			"percent": 90,
			"feedback": f"Installing Blender {version}"
		}
		self.install_process = self.__exec(["sudo", "mv", f"blender-{version}-{platform}", OPT_DIR])
		
		# Finish process.
		self.__get_installed_versions()
		self.window.state.install_process = {
			"percent": 100,
			"feedback": f"Blender {version} successfully installed!"
		}
	
	def install_version_on_window(self, version:str) -> None:
		# TODO: Check the CPU architecture (x64 or ARM).
		installer:str = "windows-x64.msix"
		self.__download_version(version, passw, installer)
	
	def remove_version_on_linux(self, version:str, passw:str) -> None:
		remove_process = self.__exec([
			"sudo", "rm", "-rf", f"{OPT_DIR}/blender-{version}-linux-x64"
		],
		no_parent=True,
		stdout=subprocess.PIPE,
		text=True)

		for line in remove_process.stdout:
			percent:int = 25
			percent_bar:list = line.strip().split()
			
			if percent_bar[1]:
				percent = int(percent_bar[1].split(".")[0])
		
			self.window.state.remove_process = {
				"percent": percent,
				"feedback": f"Removing Blender {version}"
			}
		
		self.__get_installed_versions()
		self.window.state.remove_process = {
			"percent": 100,
			"feedback": f"Blender {version} removed successfully!"
		}

	def remove_version_on_windows(self, version:str) -> None:
		pass