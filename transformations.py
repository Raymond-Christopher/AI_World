"""Defines the TransformTemplate class used for modeling scalable resource
transformations."""


class TransformTemplate:
    """TransformTemplate represents a template for data transformations,
    encapsulating a name, input mappings, and output mappings.

    This class allows for the scaling of input and output values by a
    given factor, producing a new TransformTemplate instance with the
    scaled values.
    :param name: The name of the transformation template.
    :type name: str
    :param inputs: A dictionary mapping input names to their values.
    :type inputs: dict
    :param outputs: A dictionary mapping output names to their values.
    :type outputs: dict :method scale: Scales all input and output
        values by the specified factor.
    :param factor: The factor by which to scale the input and output
        values.
    :type factor: int
    :return: A new TransformTemplate instance with scaled inputs and
        outputs.
    :rtype: TransformTemplate
    """

    def __init__(self, name: str, inputs: dict, outputs: dict):
        """
        Initialize a TransformTemplate.

        Args:
            name (str): The name of the transformation.
            inputs (dict): Input resources and their quantities.
            outputs (dict): Output resources and their quantities.
        """
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def scale(self, factor: int):
        """
        Return a new TransformTemplate with all input and output quantities scaled by the given factor.

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
