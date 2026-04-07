import os
import time
import webview

import src.blender as blender
import src.utils as utils
from src.locations import LOCAL_APP_DATA, PROJECTS_DATA

class Projects:
	def __init__(self):
		self.data:list = []
		self.__load_all_projects()

	def __load_all_projects(self) -> None:
		os.makedirs(LOCAL_APP_DATA, exist_ok=True)
		if os.path.exists(PROJECTS_DATA):
			with open(PROJECTS_DATA, "r") as file:
				projects:dict = {}
				for line in file:
					filepath, modified_time, version = line.strip().split(";")
					if os.path.exists(filepath):
						path, filename = os.path.split(filepath)					
						projects[float(modified_time)] = {
							"filepath": filepath,
							"filename": filename,
							"path": path,
							"modified": time.ctime(float(modified_time)),
							"modified_time": modified_time,
							"version": version
						}
				
				self.data = [
					value for key, value
					in sorted(projects.items(), reverse=True)
				]
	
	def __dump_all_projects(self) -> None:
		os.makedirs(LOCAL_APP_DATA, exist_ok=True)

		entries:list = [
			f"{p["filepath"]};{p["modified_time"]};{p["version"]}\n"
			for p in self.data
		]
		
		with open(PROJECTS_DATA, "w") as file:
			file.writelines(entries)

	def add_created_project(self, project:dict) -> None:
		filepath:str = os.path.join(project["path"], f"{project["filename"]}.blend")

		with open(PROJECTS_DATA, "a") as file:
			file.write(f"{filepath};{time.time()};{project["version"]}\n")

		self.__load_all_projects()
	
	def add_projects(self, projects:list, installed_versions:list, exec_path:str) -> None:
		stored_projects:list = [project["filepath"] for project in self.data]
		entries:list = []

		webview.windows[0].state.import_process = {
			"percent": 0,
			"feedback": "Loading projects"
		}
		
		import_dialog_data:dict = {
			"title": "Importing projects",
		}
		utils.exec_on_gui("importProjects", import_dialog_data)
		
		import_index:int = 0
		for filepath in projects:
			if filepath not in stored_projects:
				webview.windows[0].state.import_process = {
					"percent": int(import_index * 100 / len(projects)),
					"feedback": f"Importing {os.path.basename(filepath)}"
				}
				
				prefix:str = blender.check_version(exec_path, filepath)
				full_version:str = next(
					(version for version in installed_versions if prefix in version),
					installed_versions[0]
				)

				entries.append(f"{filepath};{time.time()};{full_version}\n")

				import_index += 1
		
		with open(PROJECTS_DATA, "a") as file:
			file.writelines(entries)
		
		self.__load_all_projects()

		webview.windows[0].state.import_process = {
			"percent": 100,
			"feedback": "All projects successfully imported"
		}
	
	def delete_project(self, project:dict) -> None:
		for p in self.data:
			if p["modified_time"] == project["modified_time"]:
				self.data.remove(p)
				break
		
		self.__dump_all_projects()
	
	def update_project(self, project:dict) -> None:
		self.delete_project(project)

		modified:float = time.time()
		self.data.insert(0, project)
		self.data[0]["modified"] = time.ctime(modified)
		self.data[0]["modified_time"] = modified

		self.__dump_all_projects()
