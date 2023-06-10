# source: https://www.airnow.gov/sites/default/files/custom-js/aqi-conc.js

US = 'US'
CHINA = 'CHINA'
PM25 = 'pm25'
PM10 = 'pm10'
O3 = 'o3'
CO = 'co'
NO2 = 'no2'
SO2 = 'so2'
# Units:
# PM2.5 - µg/m3
# PM10 - µg/m3
# NO2 - ppb
# O3 - ppb
# CO - ppm
# SO2 - ppb


# Pollutant EC | WHO
# Ozone 1 ppb = 1.9957 μg m-3 1 ppb = 1.96 μg m-3
# Nitrogen dioxide 1 ppb = 1.9125 μg m-3 1 ppb = 1.88 μg m-3
# Carbon monoxide 1 ppm = 1.1642 mg m-3 1 ppm = 1.15 mg m-3
# Sulphur dioxide 1 ppb = 2.6609 μg m-3 1 ppb = 2.62 μg m-3
# Benzene 1 ppb = 3.2430 μg m-3 1 ppb = 3.19 μg m-3
# 1,3-butadiene 1 ppb = 2.2452 μg m-3 1 ppb = 2.21 μg m-3


CONVERSIONS = {
    PM25: {
        CHINA: [# AQI, #Concentration
                    (0, 0),
                    (50, 35),
                    (100, 75),
                    (150, 115),
                    (200, 150),
                    (300, 250),
                    (400, 350),
                    (500, 500)
                ],
        US: [# AQI, #Concentration
                (0, 0),
                (50, 12),
                (100, 35.4),
                (150, 55.4),
                (200, 150.4),
                (400, 350.4),
                (500, 500)
            ]
    },
    PM10 : {
        US:[# AQI, #PM10 concentrations
                (0, 0),
                (50, 54),
                (100, 154),
                (150, 254),
                (200, 354),
                (300, 424),
                (400, 504),
                (500, 604)
            ]
    },
    O3: {
        US: [
            (0, 0),
            (50, 54),
            (100, 70),
            (150, 85),
            (200, 105),
            (300, 200),
        ]
    },
    CO: {
        US: [
            (0, 0),
            (50, 4.4),
            (100, 9.4),
            (150, 12.4),
            (200, 15.4),
            (300, 30.4),
            (400, 40.4),
            (500, 50.4)
        ]
    },
    NO2: {
        US: [
            (0, 0),
            (50, 53),
            (100, 100),
            (150, 360),
            (200, 649),
            (300, 1244),
            (400, 1644),
            (500, 2044)
        ]
    },
    SO2: {
        US: [
            (0, 0),
            (50, 35),
            (100, 75),
            (150, 185),
            (200, 304)
        ]
    },
    
}

def _interpolate(val, standard, pollutant, reverse=False):
    vals = CONVERSIONS[pollutant][standard]
    if reverse:
        vals = [t[::-1] for t in vals]

    for i, (x, y) in enumerate(vals):
        if x < val:
            continue
        x_1, y_1 = vals[i-1]
        return y + float(val - x)/(x - x_1)*(y - y_1)

    # above 500, 1:1 conversion
    return val

def to_aqi(val, standard, pollutant):
    return round(_interpolate(val, standard, pollutant, True))

def from_aqi(val, standard, pollutant):
    return round(_interpolate(val, standard, pollutant, False))

def china_aqi_to_concentration(china_aqi):
    return round(_interpolate(china_aqi, CHINA, PM25))

def concentration_to_china_aqi(conc):
    return round(_interpolate(conc, CHINA, PM25, True))

def us_aqi_to_concentration(us_aqi):
    return _interpolate(us_aqi, US, PM25)

def concentration_to_us_aqi(conc):
    return round(_interpolate(conc, US, PM25, True))

def china_aqi_to_us_aqi(china_aqi):
    conc = china_aqi_to_concentration(china_aqi)
    return concentration_to_us_aqi(conc)

def us_aqi_to_china_aqi(us_aqi):
    conc = us_aqi_to_concentration(us_aqi)
    return concentration_to_china_aqi(conc)

def us_aqi_to_pm10_concentration(us_aqi):
    return _interpolate(us_aqi, US, PM10)

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
