import sys
import requests
from src.locations import *

def dev_mode(window_config) -> None:
	dev_ui_path = "http://localhost:5173"

	# Check if the UI is running locally.
	try:
		response = requests.get(dev_ui_path, timeout=5)
		if response.status_code == 200:
			window_config["url"] = dev_ui_path
			print(f"Dev mode selected. Listening to {dev_ui_path}")
			if "--debug" in sys.argv:
				config["debug"] = True
		else:
			print("No local ui detected! Running normal mode.")
	except requests.exceptions.RequestException as e:
		print(e)

	# Verbose mode
	if "-v" in sys.argv or "--verbose" in sys.argv:
		print(f"OS_PLATFORM: {OS_PLATFORM}")
		print(f"HOME_DIR: {HOME_DIR}")
		print(f"USER_DOCS_DIR: {USER_DOCS_DIR}")
		print(f"LOCAL_APP_DATA: {LOCAL_APP_DATA}")
		print(f"PROJECTS_DATA: {PROJECTS_DATA}")
		print(f"RELEASES_DATA: {RELEASES_DATA}")
