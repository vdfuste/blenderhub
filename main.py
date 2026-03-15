import os
import sys
import webview
from src.api import BHApi

ui_path = os.path.abspath("ui/dist/index.html")
config = { "gui": "qt" }

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


bhapi = BHApi()

window = webview.create_window("Blender Hub v0.1.0", ui_path, js_api=bhapi)
bhapi.set_window(window)

webview.start(**config)
