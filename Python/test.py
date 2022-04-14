from aqi_conversions import *

# Tests
import unittest

class TestChinaAQIs(unittest.TestCase):

    def test_to_conc(self):
        self.assertEqual(china_aqi_to_concentration(50), 35.0)
        self.assertEqual(china_aqi_to_concentration(500), 500)
        self.assertEqual(china_aqi_to_concentration(600), 600)
        self.assertEqual(china_aqi_to_concentration(250), 200)

    def test_to_aqi(self):
        self.assertEqual(concentration_to_china_aqi(35), 50)
        self.assertEqual(concentration_to_china_aqi(500), 500)
        self.assertEqual(concentration_to_china_aqi(600), 600)
        self.assertEqual(concentration_to_china_aqi(200), 250)
        
    def test_us_aqi_to_china_aqi(self):
        self.assertEqual(us_aqi_to_china_aqi(99), 50)

class TestUSAQIs(unittest.TestCase):

    def test_to_conc(self):
        self.assertEqual(us_aqi_to_concentration(50), 12.0)
        self.assertEqual(us_aqi_to_concentration(500), 500)
        self.assertEqual(us_aqi_to_concentration(600), 600)
        self.assertEqual(us_aqi_to_concentration(351), 301.4)

    def test_to_aqi(self):
        self.assertEqual(concentration_to_us_aqi(12), 50)
        self.assertEqual(concentration_to_us_aqi(500), 500)
        self.assertEqual(concentration_to_us_aqi(600), 600)
        self.assertEqual(concentration_to_us_aqi(301.4), 351)
    
    def test_china_to_us_aqi(self):
        self.assertEqual(china_aqi_to_us_aqi(50), 99)

if __name__ == '__main__':
    unittest.main()
