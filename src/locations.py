import os
import sys

APP_DIR_NAME:str = "Blender Hub"
UI_PATH:str = os.path.abspath("ui/dist/index.html")

OS_PLATFORM:str = sys.platform
HOME_DIR:str = os.path.expanduser("~")
USER_DOCS_DIR:str = os.path.join(HOME_DIR, "Documents")

if OS_PLATFORM == "linux":
	APP_DIR_NAME = "blenderhub"

	SHARED_DATA:str = os.path.join("/var/lib", APP_DIR_NAME)
	INSTALLS_DIR:str = os.path.join(SHARED_DATA, "versions")
	LOCAL_APP_DATA:str = os.path.join(HOME_DIR, ".local", "share", APP_DIR_NAME)

elif "win" in OS_PLATFORM:
	OS_PLATFORM = "windows"

	SHARED_DATA:str = os.path.join(os.getenv("PROGRAMDATA"), APP_DIR_NAME)
	INSTALLS_DIR:str = os.path.join(SHARED_DATA, "versions")
	LOCAL_APP_DATA:str = os.path.join(os.getenv("LOCALAPPDATA"), APP_DIR_NAME)

elif OS_PLATFORM == "macos":
	SHARED_DATA:str = os.path.join("/Library/Application/Support", APP_DIR_NAME)
	INSTALLS_DIR:str = os.path.join(SHARED_DATA, "versions")
	LOCAL_APP_DATA:str = os.path.join(HOME_DIR, "Library", "Application Support", APP_DIR_NAME)

else:
	print(f"Looks like your operating system is not supported.")
	print("Please contact me and I'll try to figure out why is not working.")
	# TODO: Add contact info.
	sys.exit()

RELEASES_DATA:str = os.path.join(SHARED_DATA, "releases.json")
PROJECTS_DATA:str = os.path.join(LOCAL_APP_DATA, "projects.txt")

if __name__ == "__main__":
	print(f"OS: {OS_PLATFORM}")
	print(f"Shared data: {SHARED_DATA}")
	print(f"Local data: {LOCAL_APP_DATA}")
	print(f"Documents folder: {USER_DOCS_DIR}")
	print(f"Blender installs folder: {INSTALLS_DIR}")