"""Unit tests for CSV parsing utility functions in csv_parser.py."""

import unittest
from unittest.mock import patch
import io
from parsers.csv_parser import parse_country_resources, parse_resource_weights


class TestCSVParsers(unittest.TestCase):
    """Test suite for CSV parsing functions."""

    def test_parse_country_resources(self):
        """Test parsing of country resource data from a CSV string.

        :return: None
        :rtype: None
        """
        csv_data = """Country,Population,Food,Water
Atlantis,100,50,30
Carpania,80,40,25
"""
        with patch("builtins.open", return_value=io.StringIO(csv_data)):
            result = parse_country_resources("dummy.csv")

        expected = {
            "Atlantis": {"Population": 100, "Food": 50, "Water": 30},
            "Carpania": {"Population": 80, "Food": 40, "Water": 25},
        }
        self.assertEqual(result, expected)

    def test_parse_resource_weights(self):
        """Test parsing of resource weight data from a CSV string.

        :return: None
        :rtype: None
        """
        csv_data = """Resource,Weight
Population,0
Food,3
Water,2
"""
        with patch("builtins.open", return_value=io.StringIO(csv_data)):
            result = parse_resource_weights("dummy.csv")

        expected = {"Population": 0.0, "Food": 3.0, "Water": 2.0}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
