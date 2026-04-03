import src.utils as utils

def check_version(exec_path:str, filepath:str):
	result:str = utils.execute(
		[exec_path, "--background", filepath, "--python", "src/blender/version.py"],
		text=True
	)
	
	output = result.stdout
	print(output)

	return "0.0.0"

def create_project(exec_path:str, filepath:str) -> None:
	result:str = utils.execute(
		[exec_path, "--background", "--python", "src/blender/create.py", "--", filepath],
	)
