import os
import sys

OS_PLATFORM = sys.platform
HOME_DIR = os.path.expanduser("~")
LOCAL_DIR_NAME = "blenderhub"

if OS_PLATFORM == "linux":
	INSTALLS_DIR = "/opt/blender"

	USER_DOCS_DIR = os.path.join(HOME_DIR, "Documents")
	LOCAL_APP_DATA = os.path.join(HOME_DIR, ".local", "share", LOCAL_DIR_NAME)

	PROJECTS_DATA = os.path.join(LOCAL_APP_DATA, "projects.txt")
	RELEASES_DATA = os.path.join(LOCAL_APP_DATA, "releases.json")

elif "win" in OS_PLATFORM:
	OS_PLATFORM = "windows"
	INSTALLS_DIR = "C:\\Program Files\\Blender Foundation"

	USER_DOCS_DIR = os.path.join(HOME_DIR, "Documents")
	LOCAL_APP_DATA = os.path.join(os.getenv("LOCALAPPDATA"), LOCAL_DIR_NAME)

	PROJECTS_DATA = os.path.join(LOCAL_APP_DATA, "projects.txt")
	RELEASES_DATA = os.path.join(LOCAL_APP_DATA, "releases.json")

#elif OS_PLATFORM == "macos":
#	pass

else:
	print(f"Looks like your operating system is not supported.")
	print("Please send me a message or something and I'll try to figure out why is not working.")
	# TODO: Add contact info.
	sys.exit()

if __name__ == "__main__":
	print(f"OS: {OS_PLATFORM}")
	print(f"Blender installs folder: {INSTALLS_DIR}")
	print(f"Documents folder: {USER_DOCS_DIR}")
	print(f"Local data: {LOCAL_APP_DATA}")