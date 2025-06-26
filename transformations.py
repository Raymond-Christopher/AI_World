class TransformTemplate:
    """Represents a transformation operation template with inputs and outputs."""

    def __init__(self, name: str, inputs: dict, outputs: dict):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def scale(self, factor: int):
        """Returns a new TransformTemplate scaled by the given factor."""
        scaled_inputs = {k: v * factor for k, v in self.inputs.items()}
        scaled_outputs = {k: v * factor for k, v in self.outputs.items()}
        return TransformTemplate(self.name, scaled_inputs, scaled_outputs)

    def __repr__(self):
        return f"<TransformTemplate name={self.name}>"
