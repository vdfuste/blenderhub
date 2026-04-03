import hashlib
import json
import subprocess
import webview

from src.locations import OS_PLATFORM

def execute(commands, *, no_parent=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs):
		try:
			func = subprocess.Popen if no_parent else subprocess.run
			return func(commands, stdout=stdout, stderr=stderr, **kwargs)
		except subprocess.CalledProcessError as e:
			print(f"Error executing commands: {e}")

def exec_on_gui(method:str, args:str, callback=None):
		execute:str = f"{method}({args})"
		#print(execute)
		return webview.windows[0].evaluate_js(execute, callback)

def download_releases_data() -> dict:
	# TODO: Get the actual data from gist.
	#blenderhub-data-versions.json
	#https://gist.github.com/vdfuste/393040a7d4383f75e0842de8c3f4dad4#file-blenderhub-data-versions-json
	# https://gist.githubusercontent.com/vdfuste/393040a7d4383f75e0842de8c3f4dad4/raw/0679940b57a1791169a853d251a7b75cd0f1ab58/blenderhub-data-versions.json
	# "0679940b57a1791169a853d251a7b75cd0f1ab58" is the timestamp token of the current version. When the gist is updated this token will change. 

	# if os.path.isfile(RELEASES_DATA):
	# 	with open(RELEASES_DATA, "r") as file:
	# 		data = json.load(file)
	# else:
	# 	pass
	
	with open("dev/_data_versions.json", "r") as file:
		mock_local_data:dict = json.load(file)

	return mock_local_data[OS_PLATFORM]

def check_passw(passw:str) -> bool:
	try:
		subprocess.run(["sudo", "-K"])
		subprocess.run(
			["sudo", "-S", "true"],
			input=passw.encode(),
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
			text=False,
			check=True
		)
		return True
	except subprocess.CalledProcessError:
		return False

def generate_checksum(filename, algorithm="md5", chunk_size=8192) -> str:
	try:
		hash = hashlib.new(algorithm)
		with open(filename, "rb") as file:
			while True:
				chunck = file.read(chunk_size)
				if not chunck: break
				hash.update(chunck)
		return hash.hexdigest()
	except Exception as e:
		print(f"Error generating the checksum: {e}")
		return ""
