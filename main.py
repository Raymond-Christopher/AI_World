"""Main script to test state quality and simulate operations."""

import copy
from evaluations.state_quality import compute_state_quality
from models.world_model import Country, World
from transformations.transformations import TransformTemplate
from evaluations.schedule_evaluation import (compute_discounted_reward, compute_undiscounted_reward)


def main():
    """Run a simulation of state quality and resource transformation between
    countries."""
    atlantis_resources = {
        "Population": 100,
        "Housing": 20,
        "HousingWaste": 3,
        "Electronics": 10,
        "ElectronicsWaste": 1,
        "MetallicAlloys": 15,
        "MetallicAlloysWaste": 2,
        "Timber": 40,
        "MetallicElements": 30,
        "Food": 60,
        "Water": 80,
        "FoodWaste": 4,
    }

    carpania_resources = {
        "Population": 80,
        "Housing": 15,
        "HousingWaste": 2,
        "Electronics": 8,
        "ElectronicsWaste": 1,
        "MetallicAlloys": 3,
        "MetallicAlloysWaste": 1,
        "Timber": 20,
        "MetallicElements": 15,
        "Food": 40,
        "Water": 60,
        "FoodWaste": 3,
    }

    atlantis = Country("Atlantis", atlantis_resources)
    carpania = Country("Carpania", carpania_resources)
    world = World([atlantis, carpania])

    # Initial state quality
    print("--- Initial State Quality ---")
    for country in world.all_countries():
        score = compute_state_quality(country.resources)
        print(f"{country.name}: {score:.2f}")

    # Transfer
    transfer_items = [("Timber", 10), ("Food", 5), ("Water", 15)]
    world.transfer_resources("Carpania", "Atlantis", transfer_items)

    atlantis_before = copy.deepcopy(atlantis)

    # Transform
    print("\n--- Attempting Housing Transform ---")
    housing_transform = TransformTemplate(
        name="Housing",
        inputs={"Population": 5, "MetallicElements": 1, "Timber": 5, "MetallicAlloys": 3},
        outputs={"Housing": 1, "HousingWaste": 1, "Population": 5},
    )

    scaled_transform = housing_transform.scale(3)
    if atlantis.has_resources(scaled_transform.inputs):
        atlantis.apply_transform(scaled_transform.inputs, scaled_transform.outputs)
        print("Transform applied.")
        reward = compute_discounted_reward(atlantis_before, atlantis, steps=2, gamma=0.95)
        print(f"Discounted reward for Atlantis: {reward:.2f}")
    else:
        print("Not enough resources for transform.")

    print("\n--- After Transform ---")
    for country in world.all_countries():
        score = compute_state_quality(country.resources)
        print(f"{country.name}: {score:.2f}")
    _ =compute_undiscounted_reward

if __name__ == "__main__":
    main()
