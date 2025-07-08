import unittest
from functions.computed_property import computed_property
import pydoc
from math import sqrt


class TestComputedProperty(unittest.TestCase):

    class Vector:
        def __init__(self, x, y, z, color=None):
            self.x, self.y, self.z = x, y, z
            self.color = color
            self.calculated = 0

        @computed_property('x', 'y', 'z', 'teste')
        def magnitude(self):
            """"Calculate magnitude of a vector and sum one to self.calculated
            everytime it is calculated from scratch"""
            self.calculated += 1
            return sqrt(self.x**2 + self.y**2 + self.z**2)

        @magnitude.setter
        def magnitude(self, new_mag):
            scale = new_mag / self.magnitude
            self.x *= scale
            self.y *= scale
            self.z *= scale

        @magnitude.deleter
        def magnitude(self):
            self.magnitude = 0

    class Circle:
        def __init__(self, radius=1):
            self.radius = radius

        @computed_property('radius')
        def diameter(self):
            return self.radius * 2

    def test_getter(self):
        vector = self.Vector(9, 2, 6)
        self.assertEqual(11, vector.magnitude)

    def test_setter(self):
        vector = self.Vector(1, 2, 2)
        vector.magnitude = 18
        self.assertEqual(6.0, vector.x)
        self.assertEqual(12.0, vector.y)
        self.assertEqual(12.0, vector.z)
        self.assertEqual(18, vector.magnitude)

    def test_deleter(self):
        vector = self.Vector(9, 2, 6)
        del vector.magnitude
        self.assertEqual(0, vector.magnitude)

    def test_docstring(self):
        docstring = pydoc.render_doc(self.Vector)
        self.assertTrue("Calculate magnitude" in docstring)

    def test_no_setter_defined(self):
        circle = self.Circle()
        with self.assertRaises(AttributeError):
            circle.diameter = 4

    def test_no_deleter_defined(self):
        circle = self.Circle()
        with self.assertRaises(AttributeError):
            del circle.diameter

    def test_recalculate(self):
        vector = self.Vector(5, 6, 7)
        m = vector.magnitude
        n = vector.magnitude
        vector.z = 5
        p = vector.magnitude
        self.assertEqual(2, vector.calculated)

    def test_dont_recalculate(self):
        vector = self.Vector(1, 3, 5)
        _ = vector.magnitude
        _ = vector.magnitude
        self.assertEqual(1, vector.calculated)

if __name__ == '__main__':
    unittest.main()
