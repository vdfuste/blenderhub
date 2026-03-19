import os
import sys
import webview

import src.utils as utils
from src.api.projects import Projects
from src.api.versions import Versions
from src.locations import OS_PLATFORM, USER_DOCS_DIR

class BHApi:
	def __init__(self) -> None:
		self.projects = Projects()
		self.versions = Versions()
	
	def __exec_on_gui(self, method:str, *args:list, callback=None):
		parse = lambda arg: f"'{arg}'" if type(arg) is str else str(arg)
		execute:str = f"{method}({','.join(map(parse, args))})"
		#print(execute)

		return webview.windows[0].evaluate_js(execute, callback)
	
	def get_init_data(self) -> dict:
		return {
			"installedVersions": self.versions.installed,
			"releases": self.versions.releases_ui,
			"projects": self.projects.data,
			"userDocs": USER_DOCS_DIR,
		}
	
	def print_log(self, data) -> None:
		print(data)

	def refresh_ui(self) -> None:
		self.__exec_on_gui("updateData", self.get_init_data())
	
	def close_app(self) -> None:
		webview.windows[0].destroy()
		sys.exit()
	
	# PROJECTS STUFF
	def create_new_project(self, data:dict) -> None:
		is_created:bool = self.versions.create_project(data)
		if is_created:
			self.projects.add_created_project(data)
			self.refresh_ui()
			self.versions.open_project(self.projects.data[0])
	
	def get_folder_location(self, current_location:str) -> str:
		result = webview.windows[0].create_file_dialog(webview.FileDialog.FOLDER, directory=current_location)
		return result[0] if result else current_location
	
	def import_projects(self) -> None:
		result = webview.windows[0].create_file_dialog(
			webview.FileDialog.OPEN,
			directory=USER_DOCS_DIR,
			allow_multiple=True,
			file_types=("Blender Files (*.blend)",)
		)

		highest_version:str = self.versions.installed[0] or "?.?.?"
		
		if result:
			self.projects.add_projects(result, highest_version)
			self.refresh_ui()

	def open_project(self, data:dict) -> None:
		self.versions.open_project(data)
		self.projects.update_project(data)
		self.refresh_ui()
	
	def remove_project(self, data:dict, remove_file:bool=False) -> None:
		self.projects.delete_project(data)
		self.refresh_ui()

		if remove_file:
			try:
				os.remove(data["filepath"])
			except PermissionError as e:
				print(f"{e}")
			except OSError as e:
				print(f"{e}")

	# INSTALLED VERSIONS STUFF
	def cancel_install(self) -> None:
		self.versions.install_process.terminate()
	
	def check_passw(self, passw:str) -> bool:
		is_valid:bool = utils.check_passw(passw)
		return is_valid
	
	def install_version(self, version:str, passw:str=None) -> None:
		webview.windows[0].state.install_process = {
			"percent": 0,
			"feedback": "Initializing process"
		}
		
		if OS_PLATFORM == "windows":
			install_dialog_data:dict = {
				"version": version,
				"title": f"Installing Blender {version}",
			}
			self.__exec_on_gui("installVersion", install_dialog_data)

			self.versions.install_version_on_window(version)
		else:
			if not passw:
				dialogData:dict = {
					"version": version,
					"title": f"Install Blender {version}",
					"text": f"The password is required to install Blender {version}.",
					"acceptLabel": f"Install Blender {version}",
					"execApi": "install_version"
				}
				self.__exec_on_gui("getPassword", dialogData)

			else:
				install_dialog_data:dict = {
					"version": version,
					"title": f"Installing Blender {version}",
				}
				self.__exec_on_gui("installVersion", install_dialog_data)

				self.versions.install_version_on_linux(version, passw)
	
	def open_version(self, version:str="") -> None:
		self.versions.open_version(version)

	def remove_version(self, version:str, passw:str=None) -> None:
		if OS_PLATFORM == "windows":
			self.versions.remove_version_on_window(version)
		else:
			if not passw:
				dialogData:dict = {
					"version": version,
					"title": f"Remove Blender {version}",
					"text": f"The password is required to remove Blender {version}.",
					"acceptLabel": f"Remove Blender {version}",
					"execApi": "remove_version"
				}
				self.__exec_on_gui("getPassword", dialogData)
			else:
				webview.windows[0].state.remove_process = {
					"percent": 0,
					"feedback": f"Removing Blender {version}"
				}

				remove_dialog_data:dict = {
					"version": version,
					"title": f"Removing Blender {version}",
				}
				self.__exec_on_gui("removeVersion", remove_dialog_data)

				self.versions.remove_version_on_linux(version, passw)
