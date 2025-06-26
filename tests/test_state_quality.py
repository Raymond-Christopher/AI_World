import unittest
from evaluations.state_quality import compute_state_quality

class TestStateQuality(unittest.TestCase):
    def test_typical_case(self):
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
            3.0 * 10 +         # Housing
            -2.0 * 2 +         # HousingWaste
            4.0 * 5 +          # Electronics
            -2.0 * 1 +         # ElectronicsWaste
            2.0 * 4 +          # MetallicAlloys
            -1.5 * 1 +         # MetallicAlloysWaste
            1.0 * 20 +         # Timber
            1.5 * 10 +         # MetallicElements
            3.0 * 30 +         # Food
            2.0 * 25 +         # Water
            -1.5 * 3           # FoodWaste
        )
        expected = expected_score / 100
        result = compute_state_quality(resources)
        self.assertAlmostEqual(result, expected, places=2)

    def test_missing_resources(self):
        # Should handle missing optional resources by treating them as zero
        resources = {
            "Population": 50,
            "Housing": 5,
            "Food": 10,
            "Water": 10
        }
        expected_score = (
            3.0 * 5 +
            3.0 * 10 +
            2.0 * 10
        )
        expected = expected_score / 50
        result = compute_state_quality(resources)
        self.assertAlmostEqual(result, expected, places=2)

    def test_zero_population(self):
        # Should return negative infinity
        resources = {
            "Population": 0,
            "Housing": 10,
            "Food": 20
        }
        result = compute_state_quality(resources)
        self.assertEqual(result, float("-inf"))

if __name__ == "__main__":
    unittest.main()
