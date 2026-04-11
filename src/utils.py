import hashlib
import json
import os
import subprocess
import webview

from src.locations import OS_PLATFORM, RELEASES_DATA, VERSIONS_DATA_FILEPATH

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
	# TODO: Get the actual data from blenderhub-releases.

	if os.path.isfile(RELEASES_DATA):
		with open(RELEASES_DATA, "r") as file:
			data:dict = json.load(file)
		return data
	
	with open(VERSIONS_DATA_FILEPATH, "r") as file:
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
