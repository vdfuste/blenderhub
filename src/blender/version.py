import bpy
	
major, minor, dunno = bpy.data.version
version:str = f"{major}.{minor}"

print(version)
