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
    shape = None

    def __init__(self, obj):
        self.properties = []
        self.children = []
        self.obj = obj
        self.make_properties(self.obj)
        FreeCAD.Console.PrintMessage(
            "##### %s self %s \n" % (self.name, self))
        self.add_children()
        self.make_child_group()
        self.obj.Proxy = self

    def make_child_group(self):
        if self.children:
            self.group = self.get_document().addObject(
                "App::DocumentObjectGroup", "%s-children" % self.name)
            self.group_name = self.group.Name
        for child in self.children:
            self.get_document().getObject(self.group_name).addObject(
                self.get_document().getObject(child.Name))

    def make_property(self, obj, name, type='PropertyLength', part_name='', desc=''):
        part_name = part_name or self.name
        # FreeCAD.Console.PrintMessage(
            # "##### %s make_property: %s \n" % (self.name, name))
        self.properties += [name]
        obj.addProperty("App::%s" % type, name,
                        part_name, desc)
        return obj

    def make_child(self, Child):
        FreeCAD.Console.PrintMessage("##### %s Make children\n" % self.name)
        child = self.get_document().addObject(
            "Part::FeaturePython", Child.name)
        Child(child)
        child.Proxy.make_properties(self.obj)
        child.ViewObject.Proxy = 0
        self.children.append(child)

    def add_children(self):
        pass

    def execute(self, fp):
        FreeCAD.Console.PrintMessage(
            "##### %s Recompute Python feature\n" % self.name)
        self.shape = self.create_shape(fp)
        fp.Shape = self.shape

    # Should be overrided to create the shape
    def create_shape(self, fp):
        return None

    def make_properties(self, obj):
        FreeCAD.Console.PrintMessage(
            "##### %s make_properties\n" % self.name)
        self.make_property(
            obj, "live_update", "PropertyBool", "KbePart", "Update the geometry").live_update = True

    def onChanged(self, fp, prop):
        "Do something when a property has changed"
        FreeCAD.Console.PrintMessage(
            "##### %s  Change property: %s \n" % (self.name, str(prop)))

        if prop in self.properties:
            for child in self.children:
                child = self.get_document().getObject(child.Name)
                if prop in child.PropertiesList:
                    if getattr(fp, prop) != getattr(child, prop):
                        setattr(child, prop, getattr(fp, prop))
            if fp.live_update:
                self.execute(fp)

    def get_document(self):
        doc = FreeCAD.activeDocument()
        if doc is None:
            doc = FreeCAD.newDocument()
        return doc


class Missile(KbePart):
    name = 'Missile'

    def add_children(self):
        FreeCAD.Console.PrintMessage("##### %s Add children\n" % self.name)
        self.make_child(Missile_nose)
        self.make_child(Missile_body)

    def make_properties(self, obj):
        super(Missile, self).make_properties(obj)
        "Add some custom properties to our box feature"

    def create_shape(self, fp):
        "Do something when doing a recomputation, this method is mandatory"
        # FreeCAD.Console.PrintMessage('children' + str(len(self.children)))
        return Part.makeBox(1, 1, 1)

        # return shape


class Missile_nose(KbePart):
    name = 'Missile_nose'

    def make_properties(self, obj):
        "Add some custom properties to our box feature"
        super(Missile_nose, self).make_properties(obj)
        self.make_property(obj,
                           "nose_length", "PropertyLength", "Missile_nose", "Length of the cylinder").nose_length = 5
        self.make_property(obj,
                           "nose_type", "PropertyString", "Missile_nose", "Nose type: cone or sphere").nose_type = "sphere"

    def create_shape(self, fp):
        "Do something when doing a recomputation, this method is mandatory"
        if fp.nose_type.strip() in 'sphere':
            nose = Part.makeSphere(
                2, Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), -90, 0, 360)
        else:
            nose = Part.makeCone(0, 2, fp.nose_length, Base.Vector(
                0, 0, -fp.nose_length), Base.Vector(0, 0, 1), 360)
        return nose


class Missile_body(KbePart):
    name = "missile_body"

    def make_properties(self, obj):
        super(Missile_body, self).make_properties(obj)
        self.make_property(obj,
                           "body_length", "PropertyLength", "Missile_body", "Length of the cylinder").body_length = 20
        self.make_property(obj,
                           "body_radius", "PropertyLength", "Missile_body", "Radius of the cylinder").body_radius = 2

    def create_shape(self, fp):
        "Do something when doing a recomputation, this method is mandatory"
        body = Part.makeCylinder(
            fp.body_radius, fp.body_length, Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), 360)
        return body


def makeMissileBody():
    print 'makeMissileBody'
    doc = FreeCAD.activeDocument()
    if doc is None:
        doc = FreeCAD.newDocument()
    missile_body = doc.addObject(
        "Part::FeaturePython", "Missile_body")
    Missile_nose(missile_body)
    missile_body.ViewObject.Proxy = 0


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
        # makeMissileBody()
        makeMissile()
    except Exception as e:
        print e
        pass
