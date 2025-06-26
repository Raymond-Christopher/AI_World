import unittest
from evaluations import schedule_evaluation

class DummyCountry:
    def __init__(self, resources):
        self.resources = resources

class TestScheduleEvaluation(unittest.TestCase):
    def setUp(self):
        # Patch compute_state_quality to return controlled values
        self.original_quality_fn = schedule_evaluation.compute_state_quality
        schedule_evaluation.compute_state_quality = self.fake_quality

    def tearDown(self):
        # Restore the original function
        schedule_evaluation.compute_state_quality = self.original_quality_fn

    def fake_quality(self, resources):
        # Fake deterministic state quality based on Housing and HousingWaste
        return resources.get("Housing", 0) * 5 + resources.get("HousingWaste", 0) * -2

    def test_compute_undiscounted_reward(self):
        before = DummyCountry({"Housing": 5, "HousingWaste": 1})
        after = DummyCountry({"Housing": 10, "HousingWaste": 1})
        expected = 48 - 23
        result = schedule_evaluation.compute_undiscounted_reward(before, after)
        self.assertAlmostEqual(result, expected, places=2)

    def test_compute_discounted_reward(self):
        before = DummyCountry({"Housing": 5, "HousingWaste": 1})
        after = DummyCountry({"Housing": 10, "HousingWaste": 1})
        gamma = 0.95
        steps = 2
        expected = (gamma ** steps) * (48 - 23)
        result = schedule_evaluation.compute_discounted_reward(before, after, steps=steps, gamma=gamma)
        self.assertAlmostEqual(result, expected, places=2)

if __name__ == "__main__":
    unittest.main()
