# source: https://www.airnow.gov/sites/default/files/custom-js/aqi-conc.js

CHINA_AQI_CONCENTRATIONS = [
    # AQI, #Concentration
    (0, 0),
    (50, 35),
    (100, 75),
    (150, 115),
    (200, 150),
    (300, 250),
    (400, 350),
    (500, 500)
]
US_AQI_CONCENTRATIONS = [
    # AQI, #Concentration
    (0, 0),
    (50, 12),
    (100, 35.4),
    (150, 55.4),
    (200, 150.4),
    (400, 350.4),
    (500, 500)
]

US_PM10_AQI_CONCENTRATIONS = [
    # AQI, #PM10 concentrations
    (0, 0),
    (50, 54),
    (100, 154),
    (150, 254),
    (200, 354),
    (300, 424),
    (400, 504),
    (500, 604)
]

def _interpolate(val, vals, reverse=False):
    if reverse:
        vals = [t[::-1] for t in vals]

    for i, (x, y) in enumerate(vals):
        if x < val:
            continue
        x_1, y_1 = vals[i-1]
        return y + float(val - x)/(x - x_1)*(y - y_1)

    # above 500, 1:1 conversion
    return val

def china_aqi_to_concentration(china_aqi):
    return _interpolate(china_aqi, CHINA_AQI_CONCENTRATIONS)

def concentration_to_china_aqi(conc):
    return round(_interpolate(conc, CHINA_AQI_CONCENTRATIONS, True))

def us_aqi_to_concentration(us_aqi):
    return _interpolate(us_aqi, US_AQI_CONCENTRATIONS)

def concentration_to_us_aqi(conc):
    return round(_interpolate(conc, US_AQI_CONCENTRATIONS, True))

def china_aqi_to_us_aqi(china_aqi):
    conc = china_aqi_to_concentration(china_aqi)
    return concentration_to_us_aqi(conc)

def us_aqi_to_china_aqi(us_aqi):
    conc = us_aqi_to_concentration(us_aqi)
    return concentration_to_china_aqi(conc)

def us_aqi_to_pm10_concentration(us_aqi):
    return _interpolate(us_aqi, US_PM10_AQI_CONCENTRATIONS)

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
