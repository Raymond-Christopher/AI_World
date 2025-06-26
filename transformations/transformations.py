"""Defines the TransformTemplate class used for modeling scalable resource
transformations."""


class TransformTemplate:
    """
    A reusable template for resource transformations, such as turning raw materials
    into housing, electronics, or other manufactured goods.

    Attributes:
        name (str): The name of the transformation.
        inputs (dict): A mapping of required input resources and quantities.
        outputs (dict): A mapping of output resources and quantities produced.

    Methods:
        scale(factor): Returns a new TransformTemplate scaled by the given factor.
    """

    def __init__(self, name: str, inputs: dict, outputs: dict):
        """Initialize a TransformTemplate.

        Args:
            name (str): The name of the transformation.
            inputs (dict): Input resources and their quantities.
            outputs (dict): Output resources and their quantities.
        """
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def scale(self, factor: int):
        """Return a new TransformTemplate with all input and output quantities
        scaled by the given factor.

        Args:
            factor (int): The multiplier to apply to all inputs and outputs.

        Returns:
            TransformTemplate: A new scaled transformation instance.
        """
        scaled_inputs = {k: v * factor for k, v in self.inputs.items()}
        scaled_outputs = {k: v * factor for k, v in self.outputs.items()}
        return TransformTemplate(self.name, scaled_inputs, scaled_outputs)

    def __repr__(self):
        """Return a string representation of the TransformTemplate."""
        return f"<TransformTemplate name={self.name}>"
