import FreeCAD
import Part
from FreeCAD import Base


class Missile_body():

    def __init__(self, obj):
        "Add some custom properties to our box feature"
        obj.addProperty("App::PropertyLength", "Length",
                        "Missile_body", "Length of the cylinder").Length = 1.0
        obj.addProperty(
            "App::PropertyLength", "Radius", "Missile_body", "Radius of the cylinder").Radius = 1.0
        obj.Proxy = self

    def onChanged(self, fp, prop):
        "Do something when a property has changed"
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop == 'Length' or prop == 'Radius':
            self.execute(fp)

    def execute(self, fp):
        "Do something when doing a recomputation, this method is mandatory"

        circle = Part.makeCircle(fp.Radius)
        cylinder = circle.extrude(Base.Vector(0, 0, fp.Length))
        fp.Shape = cylinder
        FreeCAD.Console.PrintMessage("Recompute Python Missile_body feature\n")


def makeMissileBody(radius=1, length=1):
        doc = FreeCAD.activeDocument()
        if doc is None:
            doc = FreeCAD.newDocument()
        missile_body = doc.addObject(
            "Part::FeaturePython", "Missile_body")
        Missile_body(missile_body)
        missile_body.ViewObject.Proxy = 0


if __name__ == "__main__":  # feature will be generated after macro execution
    makeMissileBody()
