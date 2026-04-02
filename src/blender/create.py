import bpy
import sys

filepath = sys.argv[-1]
bpy.ops.wm.save_as_mainfile(filepath=filepath)
