# This is used to start freecad from a python shell


FREECADPATH = '/usr/lib/freecad/lib'  # adapt this path to your system
import sys
# choose your favorite test to check if you are running with FreeCAD GUI
# or traditional Python
freecad_gui = True
# if not(FREECADPATH in sys.path): # test based on PYTHONPATH
if not("FreeCAD" in dir()):       # test based on loaded module
    freecad_gui = False

if not(freecad_gui):
    sys.path.append(FREECADPATH)
    import FreeCAD
