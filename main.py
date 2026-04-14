import os
import sys
import webview

from src.api import BHApi
from src.locations import OS_PLATFORM, UI_FILEPATH, VERSION_FILEPATH

with open(VERSION_FILEPATH, "r") as file:
	VERSION:str = file.readline()

bhapi = BHApi()
config = {}
window_config:dict = {
	"title": f"Blender Hub {VERSION}",
	"width": 1280,
	"height": 720,
	"background_color": "#121416",
	"url": UI_FILEPATH,
	"js_api": bhapi,
}

if OS_PLATFORM == "linux":
	config["gui"] = "qt"

def window_start() -> None:
	window = webview.create_window(**window_config)
	webview.start(**config)

if __name__ == "__main__":	
	window_start()
