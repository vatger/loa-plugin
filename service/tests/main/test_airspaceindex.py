import unittest

from main.airspaceindex import AirspaceIndex
from models.vatglasses import Airspace


class TestAirspaceIndex(unittest.TestCase):
    def setUp(self):
        data = [
            {
                "id": "Allersberg",
                "group": "EDMM",
                "uid": "ALB",
                "owner": ["ALB", "WLD", "RDG", "EGG", "ZUG"],
                "sectors": [
                    {
                        "max": 314,
                        "min": 105,
                        "points": [
                            ["491000", "0115800"],
                            ["484003", "0114739"],
                            ["484004", "0113042"],
                            ["484004", "0111915"],
                            ["490710", "0104025"],
                            ["490817", "0110757"],
                            ["491000", "0115800"],
                        ],
                    }
                ],
            }
        ]

        airspaces = [Airspace(**element) for element in data]

        self.airspace_index = AirspaceIndex(airspaces)

    def test_in(self):
        test_lat = 49.1
        test_lon = 11.5
        test_alt = 200
        result = self.airspace_index.query(lat=test_lat, lon=test_lon, alt=test_alt)

        self.assertEqual(result, "ALB")

    def test_out(self):
        test_lat = 0
        test_lon = 0
        test_alt = 0
        result = self.airspace_index.query(lat=test_lat, lon=test_lon, alt=test_alt)

        self.assertIsNone(result)

    def test_above(self):
        test_lat = 49.1
        test_lon = 11.5
        test_alt = 316
        result = self.airspace_index.query(lat=test_lat, lon=test_lon, alt=test_alt)

        self.assertIsNone(result)

    def test_below(self):
        test_lat = 49.1
        test_lon = 11.5
        test_alt = 100
        result = self.airspace_index.query(lat=test_lat, lon=test_lon, alt=test_alt)

        self.assertIsNone(result)
