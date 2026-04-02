import os
import sys

APP_DIR_NAME = "blenderhub"
HOME_DIR = os.path.expanduser("~")
OS_PLATFORM = sys.platform
UI_PATH = os.path.abspath("ui/dist/index.html")

if OS_PLATFORM == "linux":
	INSTALLS_DIR = f"/opt/{APP_DIR_NAME}"

	USER_DOCS_DIR = os.path.join(HOME_DIR, "Documents")
	LOCAL_APP_DATA = os.path.join(HOME_DIR, ".local", "share", APP_DIR_NAME)

	PROJECTS_DATA = os.path.join(LOCAL_APP_DATA, "projects.txt")
	RELEASES_DATA = os.path.join(LOCAL_APP_DATA, "releases.json")

elif "win" in OS_PLATFORM:
	OS_PLATFORM = "windows"
	INSTALLS_DIR = f"C:\\Program Files\\{APP_DIR_NAME}"

	USER_DOCS_DIR = os.path.join(HOME_DIR, "Documents")
	LOCAL_APP_DATA = os.path.join(os.getenv("LOCALAPPDATA"), APP_DIR_NAME)

	PROJECTS_DATA = os.path.join(LOCAL_APP_DATA, "projects.txt")
	RELEASES_DATA = os.path.join(LOCAL_APP_DATA, "releases.json")

elif OS_PLATFORM == "macos":
	INSTALLS_DIR = f"/Applications/{APP_DIR_NAME}.app"

	USER_DOCS_DIR = os.path.join(HOME_DIR, "Documents")
	LOCAL_APP_DATA = os.path.join(HOME_DIR, "Library", "Application Support", APP_DIR_NAME)

	PROJECTS_DATA = os.path.join(LOCAL_APP_DATA, "projects.txt")
	RELEASES_DATA = os.path.join(LOCAL_APP_DATA, "releases.json")

else:
	print(f"Looks like your operating system is not supported.")
	print("Please contact me and I'll try to figure out why is not working.")
	# TODO: Add contact info.
	sys.exit()

if __name__ == "__main__":
	print(f"OS: {OS_PLATFORM}")
	print(f"Blender installs folder: {INSTALLS_DIR}")
	print(f"Documents folder: {USER_DOCS_DIR}")
	print(f"Local data: {LOCAL_APP_DATA}")