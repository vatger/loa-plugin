import unittest

import requests
from pydantic import ValidationError

from models.vatglasses import Airspace


class TestVatglassesModel(unittest.TestCase):
    def from_api(self, url):
        data = requests.get(url).json()

        airspaces = data.get("airspace")

        for airspace in airspaces:
            try:
                Airspace(**airspace)
            except ValidationError as e:
                print(f"Validation error on {data.get('uid')}: {e}")
                raise

        self.assertTrue(len(airspaces) > 0)

    def test_from_apis(self):
        countries = ["ed"]
        url = "https://raw.githubusercontent.com/lennycolton/vatglasses-data/refs/heads/main/data/"

        for country in countries:
            self.from_api(url + country + ".json")
