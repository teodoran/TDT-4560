try:
    import FreeCAD
    from FreeCAD import Base
    import Part
except Exception, e:
    import freecad_bash_startup

from os import sys
sys.path.append('/home/simenhg/workspace/kbe-design/freecad/freeKBE/')
from freeKbe import KbePart


class Missile(KbePart):
    name = 'Missile'

    def add_children(self):
        self.make_child(Missile_nose)
        self.make_child(Missile_aft_body)
        self.make_child(Rotation_fins)

    def make_properties(self, obj):
        super(Missile, self).make_properties(obj)
        self.make_property(
            obj, 'missile_radius', 'PropertyLength').missile_radius = 2
        self.make_property(
            obj, 'missile_length', 'PropertyLength').missile_length = 20

    def create_shape(self, fp):
        "Do something when doing a recomputation, this method is mandatory"
        body = Part.makeCylinder(
            fp.missile_radius, fp.missile_length, Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), 360)
        return body


class Missile_nose(KbePart):
    name = 'Missile_nose'

    def make_properties(self, obj):
        super(Missile_nose, self).make_properties(obj)
        self.make_property(obj,
                           "nose_length", "PropertyLength").nose_length = 5
        self.make_property(obj,
                           "nose_type", "PropertyString").nose_type = "sphere"

    def create_shape(self, fp):
        if fp.nose_type.strip() in 'sphere':
            nose = Part.makeSphere(
                fp.missile_radius, Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), -90, 0, 360)
        else:
            nose = Part.makeCone(0, fp.missile_radius, fp.nose_length, Base.Vector(
                0, 0, -fp.nose_length), Base.Vector(0, 0, 1), 360)
        return nose


class Rotation_fins(KbePart):
    name = 'rotation_fins'

    def make_properties(self, obj):
        super(Rotation_fins, self).make_properties(obj)
        self.make_property(
            obj, "fin_thickness", "PropertyLength").fin_thickness = 0.5
        self.make_property(
            obj, "fin_chord", "PropertyLength").fin_chord = 3
        self.make_property(
            obj, "fin_length", "PropertyLength").fin_length = 2
        self.make_property(
            obj, "number_of_fins", "PropertyLength").number_of_fins = 5

    def create_shape(self, fp):
        shape = None
        fin_angle_offset = 360 / fp.number_of_fins
        for i in range(int(fp.number_of_fins)):
            fin = self.make_fin_profile(fp)
            fin.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 1, 0), 90)
            fin.translate(Base.Vector(fp.missile_radius, 0, 0))
            fin.translate(Base.Vector(0, 0, fp.missile_length))
            fin.rotate(
                Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), fin_angle_offset * i)
            if shape:
                shape = shape.fuse(fin)
            else:
                shape = fin
        return shape

    def make_fin_profile(self, fp):
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


class Missile_aft_body(KbePart):
    name = "missile_aft_body"

    def make_properties(self, obj):
        super(Missile_aft_body, self).make_properties(obj)
        self.make_property(obj,
                           "aft_body_length", "PropertyLength").aft_body_length = 5
        self.make_property(obj,
                           "aft_body_end_radius", "PropertyLength").aft_body_end_radius = 1.5

    def create_shape(self, fp):
        "Do something when doing a recomputation, this method is mandatory"
        aft_body = Part.makeCone(
            fp.missile_radius, fp.aft_body_end_radius, fp.aft_body_length, Base.Vector(0, 0, fp.missile_length), Base.Vector(0, 0, 1), 360)
        return aft_body


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
    except Exception as e:
        print e
