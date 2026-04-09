import os
import sys

# Adding the root directory on sys.path to handle imports correctly.
current_directory:str = os.path.dirname(__file__) 				# blenderhub/dev/
parent_directory:str = os.path.join(current_directory, '..')	# blenderhub/
sys.path.append(os.path.abspath(parent_directory)) 				# /path/to/blenderhub/

from main import *

DEV_UI_PATH:str = "http://localhost:5173"

# Help list
if "-h" in sys.argv or "--help" in sys.argv:
	print("Blender Hub Development Help:")
	
	print("\nAvailable options:")
	print(f" --local-gui        Tries to find a running terminal with the GUI on {DEV_UI_PATH}.")
	print( " --debug            Enables the debug console. Only works if --local-gui is specified.")
	print( " -v or --verbose    Prints a list of all the global paths and locations.")
	
	print("\nBuild the GUI:")
	print("To build the GUI just run 'npm run build' on the blenderhub/ui/ directory. There is no need to keep the terminal open once the GUI is built.")

	print("\nUsing the local GUI:")
	print("To use the local GUI open a new terminal and run 'npm run dev' on the blenderhub/ui/ directory and keep the terminal open.")
	print("Please make sure dev/requirements.txt are installed using 'python -m pip install dev/requirements.txt'.")
	
	sys.exit()

# Verbose mode
if "-v" in sys.argv or "--verbose" in sys.argv:
	from src.locations import *
	print(f"OS_PLATFORM: {OS_PLATFORM}")
	print(f"HOME_DIR: {HOME_DIR}")
	print(f"USER_DOCS_DIR: {USER_DOCS_DIR}")
	print(f"LOCAL_APP_DATA: {LOCAL_APP_DATA}")
	print(f"PROJECTS_DATA: {PROJECTS_DATA}")
	print(f"RELEASES_DATA: {RELEASES_DATA}")

# Use the local React UI.
if "--local-gui" in sys.argv:
	import requests

	try:
		response = requests.get(DEV_UI_PATH, timeout=5)

		if response.status_code == 200:
			window_config["url"] = DEV_UI_PATH
		
			print(f"Dev mode selected. Listening to {DEV_UI_PATH}")
		
			if "--debug" in sys.argv:
				config["debug"] = True

	except:
		print("[BH DEV MODE]: No local ui detected! Running normal mode.")
		print("To update the GUI just run 'npm run build' on the blenderhub/ui/ directory. There is no need to keep the terminal open once the GUI is built.")
		print("To use the local GUI open a new terminal and run 'npm run dev' on the blenderhub/ui/ directory and keep the terminal open.")
		print("Please make sure dev/requirements.txt are installed using 'python -m pip install dev/requirements.txt'.")

window_start()
