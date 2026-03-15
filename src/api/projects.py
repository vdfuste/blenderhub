import os
import time
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
					filepath, modified_time, version = line.strip().split(";", 2)
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
	
	def add_projects(self, projects:list, version:str) -> None:
		# TODO: Get projects version
		
		stored_projects:list = {
			p["filepath"] for p in self.data
		}

		entries:list = [
			f"{fp};{time.time()};{version}\n"
			for fp in projects if fp not in stored_projects
		]
		
		with open(PROJECTS_DATA, "a") as file:
			file.writelines(entries)
		
		self.__load_all_projects()
	
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
