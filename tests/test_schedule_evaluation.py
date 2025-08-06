"""Unit tests for reward evaluation functions in schedule_evaluation.py."""

import unittest
import math
from evaluations import schedule_evaluation
from transformations.transformations import TransformTemplate


# pylint: disable=too-few-public-methods
class DummyCountry:
    """Mock Country with basic transformation capabilities."""

    def __init__(self, name, resources):
        self.name = name
        self.resources = resources

    def has_resources(self, required):
        return all(self.resources.get(k, 0) >= v for k, v in required.items())

    def apply_transform(self, inputs, outputs):
        for k, v in inputs.items():
            self.resources[k] = self.resources.get(k, 0) - v
        for k, v in outputs.items():
            self.resources[k] = self.resources.get(k, 0) + v


class DummyWorld:
    """Mock World for testing schedule evaluation."""

    def __init__(self, countries):
        self.countries = {c.name: c for c in countries}

    def get_country(self, name):
        return self.countries[name]


class TestScheduleEvaluation(unittest.TestCase):
    """Test suite for computing undiscounted and discounted rewards."""

    def setUp(self):
        """Replace compute_state_quality with a fake version for testing."""
        self.original_quality_fn = schedule_evaluation.compute_state_quality
        schedule_evaluation.compute_state_quality = self.fake_quality

    def tearDown(self):
        """Restore the original compute_state_quality function."""
        schedule_evaluation.compute_state_quality = self.original_quality_fn

    def fake_quality(self, resources, _weights=None):
        """Mocked deterministic state quality based on Housing and HousingWaste."""
        return resources.get("Housing", 0) * 5 + resources.get("HousingWaste", 0) * -2

    def test_compute_undiscounted_reward(self):
        before = DummyCountry("A", {"Housing": 5, "HousingWaste": 1})
        after = DummyCountry("A", {"Housing": 10, "HousingWaste": 1})
        expected = 48 - 23
        result = schedule_evaluation.compute_undiscounted_reward(before, after, weights={})
        self.assertAlmostEqual(result, expected, places=2)

    def test_compute_discounted_reward(self):
        before = DummyCountry("A", {"Housing": 5, "HousingWaste": 1})
        after = DummyCountry("A", {"Housing": 10, "HousingWaste": 1})
        gamma = 0.95
        steps = 2
        expected = (gamma**steps) * (48 - 23)
        result = schedule_evaluation.compute_discounted_reward(
            before, after, steps=steps, gamma=gamma, weights={}
        )
        self.assertAlmostEqual(result, expected, places=2)

    def test_logistic_function(self):
        self.assertAlmostEqual(schedule_evaluation.logistic(0), 0.5, places=2)
        self.assertGreater(schedule_evaluation.logistic(10), 0.99)
        self.assertLess(schedule_evaluation.logistic(-10), 0.01)

    def test_compute_expected_utility(self):
        country = DummyCountry("Testia", {"Housing": 5, "HousingWaste": 1, "Population": 5})
        world = DummyWorld([country])
        transform = TransformTemplate("Housing", inputs={"Population": 5}, outputs={"Housing": 1})
        schedule = [(transform, "Testia")]

        result = schedule_evaluation.compute_expected_utility(
            schedule=schedule,
            world=world,
            country_name="Testia",
            weights={},
            gamma=0.95,
        )

        expected_logistic = 1 / (1 + math.exp(-4.75))  # expected reward = 5
        self.assertAlmostEqual(result, expected_logistic, places=2)

if __name__ == "__main__":
    unittest.main()
