import unittest
from helpers import calc_sphere_volume, Vector

class TestVectorMagnitude(unittest.TestCase):
    
    def setUp(self):
        self.v1 = Vector(3,4)
        self.v2 = Vector(5,5)
    
    def tearDown(self):
        del self.v1
        del self.v2
    
    def test_int_result(self):
        result = self.v1.magnitude()
        self.assertEqual(result, 5.0)
        v = Vector(-3, 4)
        result = v.magnitude()
        self.assertEqual(result, 5.0)
        v = Vector(3, -4)
        result = v.magnitude()
        self.assertEqual(result, 5.0)
        v = Vector(-3, -4)
        result = v.magnitude()
        self.assertEqual(result, 5.0)
    
    def test_decimal_result(self):
        v2 = Vector(5, 5)
        result = v2.magnitude()
        self.assertAlmostEqual(result, 7.071, places=3)

class TestSphereVolume(unittest.TestCase):
    def setUp(self):
        self.diameter = 8
        
    def tearDown(self):
        del self.diameter
    
    def test_positive_number(self):
        vol = calc_sphere_volume(self.diameter)
        self.assertAlmostEqual(vol, 268, places=0)

if __name__ == '__main__':
    unittest.main()