# pylint: disable=C0412, W0611
"""Main script to test state quality and simulate operations."""

import copy
from evaluations.state_quality import compute_state_quality
from models.world_model import Country, World
from transformations.transformations import TransformTemplate
from evaluations.schedule_evaluation import (
    compute_discounted_reward,
    compute_undiscounted_reward,
    compute_expected_utility,
    generate_schedules
)
from parsers.csv_parser import parse_country_resources, parse_resource_weights
from scheduler import country_scheduler
from visualizations.plot_schedule import plot_schedule_log
from visualizations.resourcetracking import plot_schedule_log


def main():
    """Run the country scheduler for a selected country."""

    # ------------------------------------------------------
    # Old simulation and transform schedule logic (commented)
    # ------------------------------------------------------
    # countries_data = parse_country_resources("data/resources.csv")
    # weights_data = parse_resource_weights("data/weights.csv")
    # atlantis = Country("Atlantis", countries_data["Atlantis"])
    # carpania = Country("Carpania", countries_data["Carpania"])
    # world = World([atlantis, carpania])
    #
    # print("--- Initial State Quality ---")
    # for country in world.all_countries():
    #     score = compute_state_quality(country.resources, weights_data)
    #     print(f"{country.name}: {score:.2f}")
    #
    # transfer_items = [("Timber", 10), ("Food", 5), ("Water", 15)]
    # world.transfer_resources("Carpania", "Atlantis", transfer_items)
    #
    # print("\n--- Attempting Best Transform Schedule ---")
    # base_transforms = [
    #     TransformTemplate(
    #         name="Housing",
    #         inputs={"Population": 5, "MetallicElements": 1, "Timber": 5, "MetallicAlloys": 1},
    #         outputs={"Housing": 4, "HousingWaste": 1, "Population": 5},
    #     ),
    # ]
    #
    # all_schedules = generate_schedules(
    #     transform_templates=base_transforms,
    #     country_name="Atlantis",
    #     max_length=2,
    #     scales=[1, 3, 5]
    # )
    #
    # best_schedule = None
    # best_utility = float('-inf')
    #
    # for schedule in all_schedules:
    #     utility = compute_expected_utility(
    #         schedule=schedule,
    #         world=world,
    #         country_name="Atlantis",
    #         weights=weights_data,
    #         gamma=0.95,
    #     )
    #     if utility > best_utility:
    #         best_utility = utility
    #         best_schedule = schedule
    #
    # if best_schedule:
    #     print(f"Best expected utility: {best_utility:.4f}")
    #     print("Best schedule:")
    #     for t, _ in best_schedule:
    #         print(f" - {t.name} x{t.inputs['Population'] // 5}") 
    #     for transform, _ in best_schedule:
    #         if atlantis.has_resources(transform.inputs):
    #             atlantis.apply_transform(transform.inputs, transform.outputs)
    #         else:
    #             print("Not enough resources to apply one of the transforms.")
    # else:
    #     print("No valid schedule found that could improve expected utility.")
    #
    # print("\n--- After Best Schedule Applied ---")
    # for country in world.all_countries():
    #     score = compute_state_quality(country.resources, weights_data)
    #     print(f"{country.name}: {score:.2f}")

    # -----------------------------------------------
    # ✅ Final scheduler: Depth-bounded, utility-driven
    # -----------------------------------------------
    print("\n--- Running Full Anytime Scheduler ---")
    country_scheduler(
        your_country_name="Atlantis",
        resources_filename="data/weights.csv",
        initial_state_filename="data/resources.csv",
        output_schedule_filename="output/schedule_atlantis.txt",
        num_output_schedules=5,
        depth_bound=3,
        frontier_max_size=100,
        track_resource_deltas=True
    )
    print("Scheduler complete. Results written to output/schedule_atlantis.txt")

    plot_schedule_log(
    json_path="output/schedule_log.json",
    output_path="output/schedule_plot.png",
    initial_resources_path="data/resources.csv"
    )   
if __name__ == "__main__":
    main()
