import unittest
from models.world_model import Country, World

class TestCountry(unittest.TestCase):
    def test_get_resource(self):
        c = Country("Testland", {"Gold": 100})
        self.assertEqual(c.get_resource("Gold"), 100)
        self.assertEqual(c.get_resource("Oil"), 0)

    def test_has_resources_true(self):
        c = Country("Resourcia", {"Food": 10, "Water": 5})
        self.assertTrue(c.has_resources({"Food": 5, "Water": 5}))

    def test_has_resources_false(self):
        c = Country("Scarcia", {"Food": 3})
        self.assertFalse(c.has_resources({"Food": 5}))

    def test_apply_transform_success(self):
        c = Country("Alchemia", {"Iron": 10, "Coal": 5})
        c.apply_transform(inputs={"Iron": 2, "Coal": 1}, outputs={"Steel": 2})
        self.assertEqual(c.get_resource("Iron"), 8)
        self.assertEqual(c.get_resource("Coal"), 4)
        self.assertEqual(c.get_resource("Steel"), 2)

    def test_apply_transform_failure(self):
        c = Country("Failia", {"Iron": 1})
        with self.assertRaises(ValueError):
            c.apply_transform(inputs={"Iron": 2}, outputs={"Steel": 1})


class TestWorld(unittest.TestCase):
    def setUp(self):
        self.country_a = Country("A", {"Gold": 50, "Food": 20})
        self.country_b = Country("B", {"Gold": 10, "Food": 5})
        self.world = World([self.country_a, self.country_b])

    def test_get_country_success(self):
        self.assertEqual(self.world.get_country("A"), self.country_a)

    def test_get_country_failure(self):
        with self.assertRaises(ValueError):
            self.world.get_country("Z")

    def test_all_countries(self):
        countries = self.world.all_countries()
        self.assertIn(self.country_a, countries)
        self.assertIn(self.country_b, countries)

    def test_transfer_resources_success(self):
        self.world.transfer_resources("A", "B", [("Gold", 10), ("Food", 5)])
        self.assertEqual(self.country_a.get_resource("Gold"), 40)
        self.assertEqual(self.country_b.get_resource("Gold"), 20)
        self.assertEqual(self.country_a.get_resource("Food"), 15)
        self.assertEqual(self.country_b.get_resource("Food"), 10)

    def test_transfer_resources_failure_insufficient(self):
        with self.assertRaises(ValueError):
            self.world.transfer_resources("A", "B", [("Gold", 100)])

    def test_transfer_resources_failure_missing_country(self):
        with self.assertRaises(ValueError):
            self.world.transfer_resources("X", "B", [("Gold", 10)])


if __name__ == "__main__":
    unittest.main()
