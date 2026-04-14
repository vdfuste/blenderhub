import os
import src.utils as utils
from src.locations import ROOT_DIR

def check_version(exec_path:str, filepath:str):
	result:str = utils.execute(
		[exec_path, "--background", filepath, "--python", os.path.join(ROOT_DIR, "src", "blender", "version.py")],
		text=True
	)
	
	output:list = result.stdout.split("\n")
	version:str = output[1]

	#print(f"{filepath.split("/")[-1]} -> {version}")

	return version

def create_project(exec_path:str, filepath:str) -> None:
	result:str = utils.execute(
		[exec_path, "--background", "--python", os.path.join(ROOT_DIR, "src", "blender", "create.py"), "--", filepath],
	)
