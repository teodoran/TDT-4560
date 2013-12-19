import random
import unittest
from mock import Mock
import freecad_bash_startup
from missile import Missile
import FreeCAD
import pdb


class DocumentMock():

    def addProperty(a, b, c, d, e):
        return True


class FeaturePythonMock():
    live_update = False
    body_length = 20
    body_radius = 2
    aft_body_length = 5
    aft_body_end_radius = 1.5
    nose_length = 5
    fin_thickness = 0.5
    fin_chord = 3
    fin_length = 2
    number_of_fins = 5
    nose_type = "sphere"


class DescribeMissile(unittest.TestCase):

    def setUp(self):
        # doc = FreeCAD.newDocument()
        # self.missile = doc.addObject(
        #     "Part::FeaturePython", "Missile")
        self.missile = DocumentMock()
        self.missile = Missile(self.missile)
        self.fp = FeaturePythonMock()

    def test_should_only_update_if_live_update_property_is_true(self):
        self.fp.live_update = True
        self.missile.execute = Mock(return_value=True)
        self.missile.onChanged(self.fp, 'body_length')
        self.assertTrue(self.missile.execute.called)
        self.fp.live_update = False
        self.missile.execute = Mock(return_value=True)
        self.missile.onChanged(self.fp, 'body_length')
        self.assertFalse(self.missile.execute.called)


if __name__ == '__main__':
    unittest.main()
