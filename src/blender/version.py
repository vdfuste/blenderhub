import bpy
	
major, minor, dunno = bpy.data.version
version:str = f"{major}.{minor}.{dunno}"

print(f"Project version: {version}")
