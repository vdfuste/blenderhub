import bpy
import sys

bpy.ops.wm.save_as_mainfile(filepath=sys.argv[-1])
