"""Unit tests for reward evaluation functions in schedule_evaluation.py."""

import unittest
from evaluations import schedule_evaluation


class DummyCountry:
    """A simple stand-in class to mock Country objects for testing."""

    def __init__(self, resources):
        """Initialize a DummyCountry with a dictionary of resources.

        :param resources: A dictionary mapping resource names to values.
        :type resources: dict
        """
        self.resources = resources


class TestScheduleEvaluation(unittest.TestCase):
    """Test suite for computing undiscounted and discounted rewards."""

    def setUp(self):
        """Patch compute_state_quality to a fake implementation for controlled
        outputs."""
        self.original_quality_fn = schedule_evaluation.compute_state_quality
        schedule_evaluation.compute_state_quality = self.fake_quality

    def tearDown(self):
        """Restore the original compute_state_quality function after tests."""
        schedule_evaluation.compute_state_quality = self.original_quality_fn

    def fake_quality(self, resources, weights=None):
        """Fake deterministic quality function based on Housing and
        HousingWaste.

        :param resources: Dictionary of resources.
        :type resources: dict
        :param weights: Ignored for testing.
        :type weights: dict or None
        :return: Mocked state quality value.
        :rtype: float
        """
        return resources.get("Housing", 0) * 5 + resources.get("HousingWaste", 0) * -2

    def test_compute_undiscounted_reward(self):
        """Test undiscounted reward calculation between two DummyCountry
        states."""
        before = DummyCountry({"Housing": 5, "HousingWaste": 1})
        after = DummyCountry({"Housing": 10, "HousingWaste": 1})
        expected = 48 - 23
        result = schedule_evaluation.compute_undiscounted_reward(before, after, weights={})
        self.assertAlmostEqual(result, expected, places=2)

    def test_compute_discounted_reward(self):
        """Test discounted reward calculation between two DummyCountry states.

        :return: None
        """
        before = DummyCountry({"Housing": 5, "HousingWaste": 1})
        after = DummyCountry({"Housing": 10, "HousingWaste": 1})
        gamma = 0.95
        steps = 2
        expected = (gamma**steps) * (48 - 23)
        result = schedule_evaluation.compute_discounted_reward(
            before, after, steps=steps, gamma=gamma, weights={}
        )
        self.assertAlmostEqual(result, expected, places=2)


if __name__ == "__main__":
    unittest.main()
