# This is for debugging
# FREECADPATH = '/usr/lib/freecad/lib'  # adapt this path to your system

# import sys
# choose your favorite test to check if you are running with FreeCAD GUI
# or traditional Python
# freecad_gui = True
# if not(FREECADPATH in sys.path): # test based on PYTHONPATH
# if not("FreeCAD" in dir()):       # test based on loaded module
#     freecad_gui = False
# print("dbg102: freecad_gui:", freecad_gui)

# if not(freecad_gui):
#     print("dbg101: add FREECADPATH to sys.path")
#     sys.path.append(FREECADPATH)
#     import FreeCAD

# END This is for debugging
try:
    import FreeCAD
    import Part
    from FreeCAD import Base
except Exception, e:
    import freecad_bash_startup


class KbePart(object):
    obj = None
    name = 'KbePart'
    properties = []
    shape = None

    def __init__(self, obj):
        obj.Proxy = self
        self.obj = obj
        self.make_property(
            "live_update", "PropertyBool", "KbePart", "Update the geometry").live_update = False

    def make_property(self, name, type='PropertyLength', part_name='', desc=''):
        part_name = part_name or self.name
        self.properties += [name]
        self.obj.addProperty("App::%s" % type, name,
                             part_name, desc)
        return self.obj

    def execute(self, fp):
        FreeCAD.Console.PrintMessage("Recompute Python Missile feature\n")
        self.shape = self.create_shape(fp)
        fp.Shape = self.shape

    # Should be overrided to create the shape
    def create_shape(self, fp):
        return None

    def onChanged(self, fp, prop):
        "Do something when a property has changed"
        # FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        #     self.execute(fp)
        if prop in self.properties:
            if fp.live_update:
                self.execute(fp)


class Missile(KbePart):
    name = 'Missile_body'

    def __init__(self, obj):
        super(Missile, self).__init__(obj)
        self.make_properties()

    def make_properties(self):
        "Add some custom properties to our box feature"
        self.make_property(
            "body_length", "PropertyLength", "Missile_body", "Length of the cylinder").body_length = 20
        self.make_property(
            "body_radius", "PropertyLength", "Missile_body", "Radius of the cylinder").body_radius = 2
        self.make_property(
            "aft_body_length", "PropertyLength", "Missile_aft_body", "Radius of the cylinder").aft_body_length = 5
        self.make_property(
            "aft_body_end_radius", "PropertyLength", "Missile_aft_body", "Radius of the cylinder").aft_body_end_radius = 1.5
        self.make_property(
            "nose_length", "PropertyLength", "Missile_nose", "Length of the cylinder").nose_length = 5
        self.make_property(
            "fin_thickness", "PropertyLength", "Missile_fin", "fin_thickness").fin_thickness = 0.5
        self.make_property(
            "fin_chord", "PropertyLength", "Missile_fin", "fin_chord").fin_chord = 3
        self.make_property(
            "fin_length", "PropertyLength", "Missile_fin", "fin_length").fin_length = 2
        self.make_property(
            "number_of_fins", "PropertyLength", "Missile_fin", "fin_length").number_of_fins = 5
        self.make_property(
            "nose_type", "PropertyString", "Missile_nose", "Nose type: cone or sphere").nose_type = "sphere"

    def create_shape(self, fp):
        "Do something when doing a recomputation, this method is mandatory"

        body = Part.makeCylinder(
            fp.body_radius, fp.body_length, Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), 360)
        aft_body = Part.makeCone(
            fp.body_radius, fp.aft_body_end_radius, fp.aft_body_length, Base.Vector(0, 0, fp.body_length), Base.Vector(0, 0, 1), 360)
        if fp.nose_type.strip() in 'sphere':
            nose = Part.makeSphere(
                fp.body_radius, Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), -90, 0, 360)
        else:
            nose = Part.makeCone(0, fp.body_radius, fp.nose_length, Base.Vector(
                0, 0, -fp.nose_length), Base.Vector(0, 0, 1), 360)
        fin_angle_offset = 360 / fp.number_of_fins
        shape = body.fuse(nose).fuse(aft_body)
        for i in range(int(fp.number_of_fins)):
            fin = make_fin_profile(fp)
            fin.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 1, 0), 90)
            fin.translate(Base.Vector(fp.body_radius, 0, 0))
            fin.translate(Base.Vector(0, 0, fp.body_length))
            fin.rotate(
                Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), fin_angle_offset * i)
            shape = shape.fuse(fin)
        return shape


def make_fin_profile(fp):
    fin_points = [Base.Vector(0, 0, 0),
                  Base.Vector(fp.fin_chord / 3, fp.fin_thickness / 2, 0),
                  Base.Vector(fp.fin_chord / 3, fp.fin_thickness / 2, 0),
                  Base.Vector(
                      (fp.fin_chord / 3) * 2, fp.fin_thickness / 2, 0),
                  Base.Vector(fp.fin_chord, 0, 0),
                  Base.Vector(
                      (fp.fin_chord / 3) * 2, -fp.fin_thickness / 2, 0),
                  Base.Vector(fp.fin_chord / 3, -fp.fin_thickness / 2, 0),
                  Base.Vector(0, 0, 0)]
    fin = Part.makePolygon(fin_points)
    fin = Part.Face(fin).extrude(
        Base.Vector(0, 0, fp.fin_length))
    return fin


def makeMissile():
    doc = FreeCAD.activeDocument()
    if doc is None:
        doc = FreeCAD.newDocument()
    missile = doc.addObject(
        "Part::FeaturePython", "Missile")
    Missile(missile)
    missile.ViewObject.Proxy = 0


if __name__ == "__main__":  # feature will be generated after macro execution
    try:
        makeMissile()
    except Exception:
        pass
