"""Defines the TransformTemplate class used for modeling scalable resource
transformations."""


class TransformTemplate:
    """A reusable template for resource transformations, such as turning raw
    materials into housing, electronics, or other manufactured goods.

    :ivar name: The name of the transformation.
    :vartype name: str
    :ivar inputs: A mapping of required input resources and quantities.
    :vartype inputs: dict
    :ivar outputs: A mapping of output resources and quantities
        produced.
    :vartype outputs: dict :method scale: Returns a new
        TransformTemplate scaled by the given factor.
    """

    def __init__(self, name: str, inputs: dict, outputs: dict):
        """Initialize a TransformTemplate.

        :param name: The name of the transformation.
        :type name: str
        :param inputs: Input resources and their quantities.
        :type inputs: dict
        :param outputs: Output resources and their quantities.
        :type outputs: dict
        """
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def scale(self, factor: int):
        """Returns a new TransformTemplate with scaled input and output
        quantities.

        All resource quantities in both `inputs` and `outputs` will be multiplied
        by the given factor to produce a new transformation.

        :param factor: The multiplier to apply to all inputs and outputs.
        :type factor: int
        :return: A new scaled transformation instance.
        :rtype: TransformTemplate
        """

        scaled_inputs = {k: v * factor for k, v in self.inputs.items()}
        scaled_outputs = {k: v * factor for k, v in self.outputs.items()}
        return TransformTemplate(self.name, scaled_inputs, scaled_outputs)

    def __repr__(self):
        """Return a string representation of the TransformTemplate."""
        return f"<TransformTemplate name={self.name}>"
