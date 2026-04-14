import os
import sys

APP_DIR_NAME:str = "Blender Hub"

ROOT_DIR:str = os.path.join(os.path.dirname(__file__), "..")
UI_FILEPATH:str = os.path.join(ROOT_DIR, "ui/dist/index.html")
VERSION_FILEPATH:str = os.path.join(ROOT_DIR, "data/version.txt")
VERSIONS_DATA_FILEPATH:str = os.path.join(ROOT_DIR, "data/_data_versions.json")

OS_PLATFORM:str = sys.platform
HOME_DIR:str = os.path.expanduser("~")

if OS_PLATFORM == "linux":
	APP_DIR_NAME = "blenderhub"

	#CONFIG_DATA:str = os.path.join("/etc", APP_DIR_NAME, "config.json")
	INSTALLS_DIR:str = os.path.join("/opt", APP_DIR_NAME, "versions")
	LOCAL_APP_DATA:str = os.path.join(HOME_DIR, ".local/share", APP_DIR_NAME)

elif "win" in OS_PLATFORM:
	OS_PLATFORM = "windows"

	#CONFIG_DATA:str = os.path.join(os.getenv("PROGRAMDATA"), APP_DIR_NAME, "config.json")
	INSTALLS_DIR:str = os.path.join(os.getenv("PROGRAMDATA"), APP_DIR_NAME, "versions")
	LOCAL_APP_DATA:str = os.path.join(os.getenv("LOCALAPPDATA"), APP_DIR_NAME)

elif OS_PLATFORM == "darwin":
	OS_PLATFORM = "macos"

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