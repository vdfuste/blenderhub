import sys
import webview

from src.api import BHApi
from src.locations import OS_PLATFORM, UI_PATH

bhapi = BHApi()
config = {}
window_config:dict = {
	"title": "Blender Hub v0.1.0",
	"width": 1280,
	"height": 720,
	"background_color": "#121416",
	"url": UI_PATH,
	"js_api": bhapi,
}

if "--dev" in sys.argv:
	from dev import dev_mode
	dev_mode(window_config)

if OS_PLATFORM == "linux":
	config["gui"] = "qt"

def init_window(window_config:dict) -> None:
	window = webview.create_window(**window_config)
	webview.start(**config)

if __name__ == "__main__":
	init_window(window_config)
