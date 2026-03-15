import os

OPT_DIR = "/opt/blender"
HOME_DIR = os.path.expanduser("~")

USER_DOCS_DIR = os.path.join(HOME_DIR, "Documents")
LOCAL_APP_DATA = os.path.join(HOME_DIR, ".local", "share", "blenderhub")

PROJECTS_DATA = os.path.join(LOCAL_APP_DATA, "projects.txt")
RELEASES_DATA = os.path.join(LOCAL_APP_DATA, "releases.json")
