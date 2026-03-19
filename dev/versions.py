import json
import os
import requests
from bs4 import BeautifulSoup

data_path:str = os.path.join(os.getcwd(), "dev/_data_versions.json")
md5_data_path:str = os.path.join(os.getcwd(), "dev/_data_md5_versions.txt")
images_data_path:str = os.path.join(os.getcwd(), "dev/_data_images_versions.json")

def get_raw_data(*, force:bool=False) -> None:
	if not force and os.path.isfile(md5_data_path):
		return
	
	# Get all available versions (from 3.0)
	repository_url:str = "https://download.blender.org/release/"

	response = BeautifulSoup(requests.get(repository_url).text, "html.parser")
	
	excludes:list = ["newpy", "alpha", "beta", "Benchmark"]
	all_versions:list = [
		link.get_text()
		for link in response.find_all("a")
		if "Blender" in link.get_text()
		and not any(
			exclude in link.get_text()
			for exclude in excludes
		)
	][66:] # 57 -> 2.79; 62 -> 2.90; 66 -> 3.0

	print("Getting all the releases data!")
	
	with open(md5_data_path, "w") as file:
		for version_folder in all_versions:
			version_url:str = repository_url + version_folder
			response = BeautifulSoup(requests.get(version_url).text, "html.parser")

			#file.write(version_folder + "\n")
			print(f"Scanning {version_folder}", end="", flush=True)
			
			# Getting md5 checksums and their filenames
			for link in response.find_all("a"):
				md5_file:str = link.get_text()
				if ".md5" in md5_file:
					md5_response = BeautifulSoup(requests.get(version_url + md5_file).text, "html.parser")

					for line in md5_response.get_text().splitlines():
						file.write(line + "\n")
			
					#file.write("\n")
				
			#file.write("\n")
			print(" Done!")

def get_images(*, force=False) -> dict:
	if not force and os.path.isfile(images_data_path):
		with open(images_data_path, "r") as file:
			return json.load(file)
	
	print("Getting all the releases images!")
	
	RELEASES_URL:str = "https://www.blender.org/download/releases/"
	IMAGE_URL_REMOVE:str = "https://www.blender.org/wp-content/uploads/"

	data:dict = {}

	response = BeautifulSoup(requests.get(RELEASES_URL).text, "html.parser")
	for link in response.find_all("a", class_="cards-item-thumbnail"):
		image_data = link.find("img")
		_, version, *lts = image_data["alt"].split()
		url_image:str = image_data["src"]

		data.setdefault(version, { "url_image": url_image.replace(IMAGE_URL_REMOVE, "") })

		if len(lts):
			data[version].update({ "lts": True })
	
	with open(images_data_path, "w") as file:
		json.dump(data, file, indent=4)
	
	print("Done!")

	return data

def get_all_versions_data() -> None:
	get_raw_data()
	images_data:dict = get_images()
	
	print("Parsing raw data to a JSON file...", end="", flush=True)
	
	data:dict = {}
	with open(md5_data_path, "r") as file:
		for line in file:
			checksum, filename = line.split()
			_, version, platform, rest = filename.split("-")
			major, minor, subversion = version.split(".")
			architecture, extension = rest.split(".", 1)

			if extension in ["msi", "zip"] or "arm" in architecture:
				continue
			
			data.setdefault(platform, {})
			data[platform].setdefault(f"serie-{major}", {})
			data[platform][f"serie-{major}"].setdefault(f"{major}.{minor}", {
				"subversions": {}
			})
			data[platform][f"serie-{major}"][f"{major}.{minor}"].update(images_data[f"{major}.{minor}"])
			data[platform][f"serie-{major}"][f"{major}.{minor}"]["subversions"].setdefault(version, {
				"checksum": checksum,
				"filename": filename,
			})
	
	with open(data_path, "w") as file:
		json.dump(data, file, indent=2)
	
	print(" Done!")

def __get_all_versions_data() -> None:
	repository_url:str = "https://download.blender.org/release/"

	# Get all available versions (from 3.0)
	response = BeautifulSoup(requests.get(repository_url).text, "html.parser")
	
	excludes:list = ["newpy", "alpha", "beta", "Benchmark"]
	all_versions:list = [
		link.get_text()
		for link in response.find_all("a")
		if "Blender" in link.get_text()
		and not any(
			exclude in link.get_text()
			for exclude in excludes
		)
	][66:] # 57 -> 2.79; 62 -> 2.90; 66 -> 3.0
	
	# Get all subversions and .md5 checksums
	data:dict = {}
	
	for version_folder in all_versions:
		version_url:str = repository_url + version_folder
		response = BeautifulSoup(requests.get(version_url).text, "html.parser")

		print(version_folder)
		
		# Getting md5 checksums and their filenames
		for link in response.find_all("a"):
			md5_file:str = link.get_text()
			if ".md5" in md5_file:
				md5_response = BeautifulSoup(requests.get(version_url + md5_file).text, "html.parser")

				for line in md5_response.get_text().splitlines():
					checksum, filename = line.split()
					_, version, platform, rest = filename.split("-")
					major, minor, subversion = version.split(".")
					architecture, extension = rest.split(".", 1)

					if extension in ["msi", "zip"] or "arm" in architecture:
						continue

					data.setdefault(platform, {})
					data[platform].setdefault(f"serie-{major}", {})
					data[platform][f"serie-{major}"].setdefault(f"{major}.{minor}", {})
					data[platform][f"serie-{major}"][f"{major}.{minor}"].setdefault(version, {
						"checksum": checksum,
						"filename": filename,
					})
					
	mock_data_path:str = os.path.join(os.getcwd(), "dev/versions.json")
	with open(mock_data_path, "w") as file:
		json.dump(data, file, indent=2)
	
if __name__ == "__main__":
	get_all_versions_data()
