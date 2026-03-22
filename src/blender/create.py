import bpy
import sys

filepath = sys.argv[-1]
print(filepath)

bpy.ops.wm.save_as_mainfile(filepath=filepath)
