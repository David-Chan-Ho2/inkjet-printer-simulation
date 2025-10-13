import unittest
from helpers import calc_velocity_magnitude

class TestVelocityMagnitude(unittest.TestCase):
    
    def test_int_result(self):
        result = calc_velocity_magnitude(3,4)
        self.assertEqual(result, 5.0)
    
    def test_negative_int_result(self):
        result = calc_velocity_magnitude(-3,4)
        self.assertEqual(result, 5.0)
        result = calc_velocity_magnitude(3,-4)
        self.assertEqual(result, 5.0)
        result = calc_velocity_magnitude(-3,-4)
        self.assertEqual(result, 5.0)
    
    def test_decimal_result(self):
        result = calc_velocity_magnitude(5,5)
        self.assertAlmostEqual(result, 7.071, places=3)


if __name__ == '__main__':
    unittest.main()