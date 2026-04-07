import src.utils as utils

def check_version(exec_path:str, filepath:str):
	result:str = utils.execute(
		[exec_path, "--background", filepath, "--python", "src/blender/version.py"],
		text=True
	)
	
	output:list = result.stdout.split("\n")
	version:str = output[1]

	#print(f"{filepath.split("/")[-1]} -> {version}")

	return version

def create_project(exec_path:str, filepath:str) -> None:
	result:str = utils.execute(
		[exec_path, "--background", "--python", "src/blender/create.py", "--", filepath],
	)
