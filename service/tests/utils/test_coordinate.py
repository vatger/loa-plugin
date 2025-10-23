import unittest

from utils.coordinate import coord_to_decimal


class TestCoordToDecimal(unittest.TestCase):
    def test_coord_conversion(self):
        test_cases = [
            # Latitude (ddmmss)
            ("491000", 49 + 10 / 60 + 0 / 3600),
            ("482600", 48 + 26 / 60 + 0 / 3600),
            ("000000", 0.0),
            ("900000", 90.0),
            ("-491000", -(49 + 10 / 60)),
            # Longitude (dddmmss)
            ("0115800", 11 + 58 / 60 + 0 / 3600),
            ("0123652", 12 + 36 / 60 + 52 / 3600),
            ("0000000", 0.0),
            ("1800000", 180.0),
            ("-0115800", -(11 + 58 / 60)),
        ]

        for coord, expected in test_cases:
            with self.subTest(coord=coord):
                print(coord, expected)
                self.assertAlmostEqual(coord_to_decimal(coord), expected, places=5)


if __name__ == "__main__":
    unittest.main()
