"""Unit tests for computing state quality based on country resources and
weights."""

import unittest
from evaluations.state_quality import compute_state_quality


class TestStateQuality(unittest.TestCase):
    """Test suite for compute_state_quality function with various scenarios."""

    def setUp(self):
        """Set up common resource weights used across multiple test cases."""
        self.weights = {
            "Housing": 3.0,
            "HousingWaste": -2.0,
            "Electronics": 4.0,
            "ElectronicsWaste": -2.0,
            "MetallicAlloys": 2.0,
            "MetallicAlloysWaste": -1.5,
            "Timber": 1.0,
            "MetallicElements": 1.5,
            "Food": 3.0,
            "Water": 2.0,
            "FoodWaste": -1.5,
        }

    def test_typical_case(self):
        """Test with a full set of expected resource values.

        :return: None
        """
        resources = {
            "Population": 100,
            "Housing": 10,
            "HousingWaste": 2,
            "Electronics": 5,
            "ElectronicsWaste": 1,
            "MetallicAlloys": 4,
            "MetallicAlloysWaste": 1,
            "Timber": 20,
            "MetallicElements": 10,
            "Food": 30,
            "Water": 25,
            "FoodWaste": 3,
        }
        expected_score = (
            3.0 * 10
            + -2.0 * 2
            + 4.0 * 5
            + -2.0 * 1
            + 2.0 * 4
            + -1.5 * 1
            + 1.0 * 20
            + 1.5 * 10
            + 3.0 * 30
            + 2.0 * 25
            + -1.5 * 3
        )
        expected = expected_score / 100
        result = compute_state_quality(resources, self.weights)
        self.assertAlmostEqual(result, expected, places=2)

    def test_missing_resources(self):
        """Test handling of missing non-required resources (assumed to be
        zero).

        :return: None
        """
        resources = {"Population": 50, "Housing": 5, "Food": 10, "Water": 10}
        expected_score = 3.0 * 5 + 3.0 * 10 + 2.0 * 10
        expected = expected_score / 50
        result = compute_state_quality(resources, self.weights)
        self.assertAlmostEqual(result, expected, places=2)

    def test_zero_population(self):
        """Test edge case where population is zero (should return negative
        infinity).

        :return: None
        """
        resources = {"Population": 0, "Housing": 10, "Food": 20}
        result = compute_state_quality(resources, self.weights)
        self.assertEqual(result, float("-inf"))


if __name__ == "__main__":
    unittest.main()
