import unittest
from mock import Mock
from missile import Missile


class DocumentMock():

    def addProperty(a, b, c, d, e):
        return True


class FeaturePythonMock():
    missile_length = 20
    missile_radius = 2
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
        self.missile = DocumentMock()
        self.missile = Missile(self.missile)
        self.fp = FeaturePythonMock()

    def test_should_be_init_with_4_children(self):
        children_length = len(self.missile.children)
        self.assertEqual(children_length, 4)

    def test_missile_should_get_properies_from_all_children(self):
        child_properies_list = [
            child.Proxy.properties for child in self.missile.children]
        for child_properies in child_properies_list:
            for prop in child_properies:
                self.assertTrue(prop in self.missile.properties)

    def test_missile_should_update_when_value_ischanged(self):
        self.fp.missile_radius = 5
        self.missile.execute = Mock(return_value=True)
        self.missile.onChanged(self.fp, 'missile_radius')
        self.assertTrue(self.missile.execute.called)

if __name__ == '__main__':
    unittest.main()
