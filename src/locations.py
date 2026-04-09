import os
import sys

APP_DIR_NAME:str = "Blender Hub"
# LOCAL_UI_PATAH:str = "_internal/ui/index.html"
UI_FILEPATH:str = os.path.join(os.path.dirname(__file__), "..", "ui/index.html")

OS_PLATFORM:str = sys.platform
HOME_DIR:str = os.path.expanduser("~")

if OS_PLATFORM == "linux":
	APP_DIR_NAME = "blenderhub"
	#UI_FILEPATH:str = os.path.join("/opt", APP_DIR_NAME, "app", LOCAL_UI_PATAH)

	#CONFIG_DATA:str = os.path.join("/etc", APP_DIR_NAME, "config.json")
	INSTALLS_DIR:str = os.path.join("/opt", APP_DIR_NAME, "versions")
	LOCAL_APP_DATA:str = os.path.join(HOME_DIR, ".local/share", APP_DIR_NAME)

elif "win" in OS_PLATFORM:
	OS_PLATFORM = "windows"
	#UI_FILEPATH:str = os.path.join("C:\\Program Files", APP_DIR_NAME, LOCAL_UI_PATAH)

	#CONFIG_DATA:str = os.path.join(os.getenv("PROGRAMDATA"), APP_DIR_NAME, "config.json")
	INSTALLS_DIR:str = os.path.join(os.getenv("PROGRAMDATA"), APP_DIR_NAME, "versions")
	LOCAL_APP_DATA:str = os.path.join(os.getenv("LOCALAPPDATA"), APP_DIR_NAME)

elif OS_PLATFORM == "darwin":
	OS_PLATFORM = "macos"
	#UI_FILEPATH:str = os.path.join("Applications", APP_DIR_NAME, LOCAL_UI_PATAH)

	#CONFIG_DATA:str = os.path.join("/Library", "Application Support", APP_DIR_NAME, "config.json")
	INSTALLS_DIR:str = os.path.join("/Applications", APP_DIR_NAME, "versions")
	LOCAL_APP_DATA:str = os.path.join(HOME_DIR, "Library", "Application Support", APP_DIR_NAME)

else:
	print("TODO: Make a proper unsupported error message.")
	sys.exit(1)

USER_DOCS_DIR:str = os.path.join(HOME_DIR, APP_DIR_NAME)
RELEASES_DATA:str = os.path.join(LOCAL_APP_DATA, "releases.json")
PROJECTS_DATA:str = os.path.join(LOCAL_APP_DATA, "projects.txt")

if __name__ == "__main__":
	print(f"OS: {OS_PLATFORM}")
	print(f"UI filepath: {UI_FILEPATH}")
	print(f"Local data: {LOCAL_APP_DATA}")
	print(f"Documents folder: {USER_DOCS_DIR}")
	print(f"Blender installs folder: {INSTALLS_DIR}")