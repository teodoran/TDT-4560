try:
    import FreeCAD
except Exception, e:
    import freecad_bash_startup

from FreeCAD import Base


class KbePart(object):
    obj = None
    name = 'KbePart'
    shape = None
    position = Base.Matrix()

    def __init__(self, obj):
        self.properties = []
        self.children = []
        self.obj = obj
        self.make_properties(self.obj)
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
        desc = desc or self.name
        self.print_msg(name)
        self.properties += [name]
        obj.addProperty("App::%s" % type, name,
                        part_name, desc)
        return obj

    def make_child(self, Child, position=None):
        child = self.get_document().addObject(
            "Part::FeaturePython", Child.name)
        self.make_properties(child)
        Child(child)
        child.Proxy.position = position or Base.Matrix()
        child.Proxy.make_properties(self.obj)
        self.properties += child.Proxy.properties
        child.ViewObject.Proxy = 0
        self.children.append(child)
        return child.Name

    def add_children(self):
        pass

    def execute(self, fp):
        self.shape = self.create_shape(fp)
        self.shape = self.shape.transformGeometry(self.position)
        fp.Shape = self.shape

    # Should be overrided to create the shape
    def create_shape(self, fp):
        return None

    def make_properties(self, obj):
        pass

    def onChanged(self, fp, prop):
        if prop in self.properties:
            for child in self.children:
                child = self.get_document().getObject(child.Name)
                if prop in child.PropertiesList:
                    if getattr(fp, prop) != getattr(child, prop):
                        setattr(child, prop, getattr(fp, prop))
                self.execute(fp)

    def get_document(self):
        doc = FreeCAD.activeDocument()
        if doc is None:
            doc = FreeCAD.newDocument()
        return doc

    def get_properties_list(self):
        return self.obj.PropertiesList

    def print_msg(self, msg):
        FreeCAD.Console.PrintMessage(
            "##### %s -  %s \n" % (
                self.name, msg))
