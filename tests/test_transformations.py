import unittest
from transformations.transformations import TransformTemplate

class TestTransformTemplate(unittest.TestCase):

    def test_initialization(self):
        transform = TransformTemplate(
            name="Housing",
            inputs={"Population": 5, "MetallicElements": 1},
            outputs={"Housing": 1, "HousingWaste": 1}
        )
        self.assertEqual(transform.name, "Housing")
        self.assertEqual(transform.inputs, {"Population": 5, "MetallicElements": 1})
        self.assertEqual(transform.outputs, {"Housing": 1, "HousingWaste": 1})

    def test_scale(self):
        transform = TransformTemplate(
            name="Housing",
            inputs={"Population": 5, "MetallicElements": 1},
            outputs={"Housing": 1, "HousingWaste": 1}
        )
        scaled = transform.scale(3)

        expected_inputs = {"Population": 15, "MetallicElements": 3}
        expected_outputs = {"Housing": 3, "HousingWaste": 3}

        self.assertEqual(scaled.name, "Housing")
        self.assertEqual(scaled.inputs, expected_inputs)
        self.assertEqual(scaled.outputs, expected_outputs)

    def test_repr(self):
        transform = TransformTemplate("Food", {}, {})
        self.assertEqual(repr(transform), "<TransformTemplate name=Food>")

if __name__ == "__main__":
    unittest.main()
