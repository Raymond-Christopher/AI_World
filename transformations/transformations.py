"""Defines the TransformTemplate class used for modeling scalable resource
transformations."""

from typing import List, Tuple
from models.world_model import World
from typing import Optional
from evaluations.state_quality import compute_state_quality


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

    def __init__(self, name: str, inputs: dict, outputs: dict, required: Optional[dict] = None):
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
        self.required = required or {}

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
        scaled_required = {k: v * factor for k, v in self.required.items()}

        return TransformTemplate(self.name, scaled_inputs, scaled_outputs,scaled_required)

    def __repr__(self):
        """Return a string representation of the TransformTemplate."""
        return f"<TransformTemplate name={self.name}, required={self.required}>"

def generate_successors(world: World, self_country: str, transform_templates: List[TransformTemplate], resource_weights: dict) -> List[Tuple[str, World, dict, float]]:
    successors = []
    self_country_obj = world.get_country(self_country)
    TRANSFER_PENALTY_FACTOR = 10
    def compute_resource_delta(old: dict, new: dict) -> dict:
        return {
            key: new.get(key, 0) - old.get(key, 0)
            for key in set(old) | set(new)
            if new.get(key, 0) != old.get(key, 0)
        }
    # Generate TRANSFORM successors
    for template in transform_templates:
        for scale_factor in range(1, 4):
            scaled = template.scale(scale_factor)
            if template.name == "Birth":
                print(f"🟡 Considering Birth x{scale_factor}")
                has_inputs = self_country_obj.has_resources(scaled.inputs)
                has_required = self_country_obj.has_resources(scaled.required)
                print(f"    Inputs available: {has_inputs}")
                print(f"    Required available: {has_required}")
                if not has_inputs or not has_required:
                    print(f"❌ Birth x{scale_factor} is NOT feasible.")
                else:
                    print(f"✅ Birth x{scale_factor} is feasible!")

            if (
                self_country_obj.has_resources(scaled.inputs)
                and self_country_obj.has_resources(scaled.required)
            ):
                new_world = world.clone()
                new_self = new_world.get_country(self_country)
                before = dict(new_self.resources)
                new_self.apply_transform(scaled.inputs, scaled.outputs)
                after = new_self.resources
                delta = compute_resource_delta(before, after)
                delta_score = sum(resource_weights.get(res, 0) * delta.get(res, 0) for res in delta)

                action_str = f"(TRANSFORM {self_country} {template.name} x{scale_factor})"
                successors.append((action_str, new_world, delta, delta_score))

                if template.name == "Birth":
                    print(f"🔥 Birth delta: {delta}, utility gain: {delta_score}")


    # Define only valid resources for transfer
    valid_transferables = {
        # Core natural and industrial resources
        "Water",
        "Food",
        "Timber",
        "MetallicElements",
        "MetallicAlloys",
        "Electronics",
        "PotentialEnergyUsable",

        # Strategic and economic resources
        "AvailableLand",
        "ConstructionMaterials",
        "Education",

        # Optional but plausible
        "SkilledLabor",
    }


   # Generate TRANSFER successors in both directions
    for other_country_obj in world.all_countries():
        other_country = other_country_obj.name
        if other_country == self_country:
            continue

        for sender_name, receiver_name in [(self_country, other_country), (other_country, self_country)]:
            sender_obj = world.get_country(sender_name)
            receiver_obj = world.get_country(receiver_name)

            for resource, amount in sender_obj.resources.items():
                if resource not in valid_transferables or amount <= 0:
                    continue

                max_transfer = min(amount, 3)
                for send_amount in range(1, int(max_transfer) + 1):
                    new_world = world.clone()

                    try:
                        sender = new_world.get_country(sender_name)
                        receiver = new_world.get_country(receiver_name)

                        cost_per_unit = resource_weights.get(resource, 1)
                        total_cost = cost_per_unit * send_amount * TRANSFER_PENALTY_FACTOR

                        if sender.resources.get("PotentialEnergyUsable", 0) < total_cost:
                            continue

                        sender.resources["PotentialEnergyUsable"] -= total_cost
                        new_world.transfer_resources(
                            sender_name=sender_name,
                            receiver_name=receiver_name,
                            resource_list=[(resource, send_amount)]
                        )

                        original_country = world.get_country(self_country)
                        new_country = new_world.get_country(self_country)

                        original_eu = compute_state_quality(original_country.resources, resource_weights)
                        new_eu = compute_state_quality(new_country.resources, resource_weights)
                        delta_score = new_eu - original_eu


                        action_str = f"(TRANSFER {sender_name} {receiver_name} (({resource} {send_amount})))"
                        delta = compute_resource_delta(sender_obj.resources, new_world.get_country(self_country).resources)
                        successors.append((action_str, new_world, delta, delta_score))

                    except ValueError:
                        continue

    return successors

