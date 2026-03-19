import os
import sys
import webview
from src.api import BHApi

ui_path = os.path.abspath("ui/dist/index.html")
config = {}

if "--dev" in sys.argv:
	import requests
	
	dev_ui_path = "http://localhost:5173"

	try:
		response = requests.get(dev_ui_path, timeout=5)

		if response.status_code == 200:
			ui_path = dev_ui_path
			print(f"Dev mode selected. Listening to {ui_path}")
			
			if "--debug" in sys.argv:
				config["debug"] = True
		else:
			print("No local ui detected! Running normal mode.")
	except requests.exceptions.RequestException as e:
		print(e)

	# Verbose mode
	if "-v" in sys.argv or "--verbose" in sys.argv:
		from src.locations import *

		print(f"OS_PLATFORM: {OS_PLATFORM}")
		print(f"HOME_DIR: {HOME_DIR}")
		print(f"USER_DOCS_DIR: {USER_DOCS_DIR}")
		print(f"LOCAL_APP_DATA: {LOCAL_APP_DATA}")
		print(f"PROJECTS_DATA: {PROJECTS_DATA}")
		print(f"RELEASES_DATA: {RELEASES_DATA}")

bhapi = BHApi()
window_config = {
	"title": "Blender Hub v0.1.0",
	"width": 1280,
	"height": 720,
	"background_color": "#121416",
	"url": ui_path,
	"js_api": bhapi,
}

window = webview.create_window(**window_config)
webview.start()
