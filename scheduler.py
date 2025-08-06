import heapq
import itertools
import os
import json
import csv

from dataclasses import dataclass
from typing import List
from models.world_model import World, Country
from transformations.transformations import generate_successors, TransformTemplate
from parsers.csv_parser import parse_country_resources, parse_resource_weights
from evaluations.state_quality import compute_state_quality

counter = itertools.count()
def load_resource_weights(path="data/weights.csv"):
    weights = {}
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            weights[row["Resource"]] = float(row["Weight"])
    return weights

@dataclass
class Schedule:
    actions: List[str]
    world: World
    eus: List[float]
    deltas: List[dict]  
    depth: int


def country_scheduler(
    your_country_name,
    resources_filename,
    initial_state_filename,
    output_schedule_filename,
    num_output_schedules,
    depth_bound,
    frontier_max_size,
    track_resource_deltas=False
):
    schedule_resource_deltas = []

    # 1. Load data
    country_data = parse_country_resources(initial_state_filename)
    weights = parse_resource_weights(resources_filename)
    countries = [Country(name, res) for name, res in country_data.items()]
    world = World(countries)

    # 2. Load transform templates
    base_transforms = [
        TransformTemplate(
            name="Housing",
            inputs={
                "AvailableLand": 1,
                "Water": 3,
                "MetallicElements": 1,
                "Timber": 4,
                "MetallicAlloys": 3,
                "PotentialEnergyUsable": 2,
            },
            outputs={
                "Housing": 3,
                "HousingWaste": 2,
            },
            required={
                "Population": 5
            }
        ),
        TransformTemplate(
            name="Alloys",
            inputs={
                "MetallicElements": 2,
                "PotentialEnergyUsable": 2,
                "Water": 2,
            },
            outputs={
                "MetallicAlloys": 3,
                "MetallicAlloysWaste": 1,
                "Water": 1,
            },
            required={
                "Population": 1
            }
        ),
        TransformTemplate(
            name="Electronics",
            inputs={
                "MetallicElements": 2,
                "MetallicAlloys": 1,
                "PotentialEnergyUsable": 2,
                "Water": 2,
            },
            outputs={
                "Electronics": 3,
                "ElectronicsWaste": 1,
            },
            required={
                "Population": 1
            }
        ),
        TransformTemplate(
            name="TrainSkilledLabor",
            inputs={
                "Population": 1,  
                "Education": 2,
                "Water": 1,
                "PotentialEnergyUsable": 2,
            },
            outputs={
                "SkilledLabor": 1
            }
        ),
        TransformTemplate(
            name="Birth",
            inputs={
                "Food": 2,
                "Water": 1,
            },
            outputs={
                "Population": 1,
                "FoodWaste": 0.5,
            },
            required={
                "Population": 2
            }
        ),
        TransformTemplate(
            name="Farm",
            inputs={
                "AvailableLand": 2,
                "Water": 5,
                "PotentialEnergyUsable": 2
            },
            outputs={
                "Food": 6,
            },
            required={
                "Population": 2,
                "SkilledLabor": 2,

            }
        ),
        TransformTemplate(
            name="MineAlloys",
            inputs={
                "PotentialEnergyUsable": 2,
                "Water": 2
            },
            outputs={
                "MetallicAlloys": 3,
                "MetallicAlloysWaste": 1
            },
            required={
                "SkilledLabor": 2,
                "Factories": 1
            }
        ),
        TransformTemplate(
            name="ExtractWater",
            inputs={
                "PotentialEnergyUsable": 4
            },
            outputs={
                "Water": 5
            },
            required={
                "Population": 1,
                "SkilledLabor": 1

            }
        ),
        TransformTemplate(
            name="Lumber",
            inputs={
                "AvailableLand": 1,
                "PotentialEnergyUsable": 1
            },
            outputs={
                "Timber": 10
            },
            required={
                "Population": 1,
            }
        ),
        TransformTemplate(
            name="BurnTimber",
            inputs={
                "Timber": 5,
            },
            outputs={
                "PotentialEnergyUsable": 2,
                "AvailableLand": -0.2
            },
            required={
                "Population": 1,
                "SkilledLabor": 1

            }
        ),
        TransformTemplate(
            name="SolarPower",
            inputs={
                "Electronics": 1
            },
            outputs={
                "PotentialEnergyUsable": 1
            },
            required={
                "SkilledLabor": 1,
                "AvailableLand": 1
            }
        ),

        TransformTemplate(
            name="HydroPower",
            inputs={},
            outputs={
                "PotentialEnergyUsable": 1
            },
            required={
                "Water": 5,
                "Population": 2,
                "Dam": 1
            }
        ),
        TransformTemplate(
            name="BuildDam",
            inputs={
                "Timber": 10,
                "MetallicAlloys": 10,
                "MetallicElements": 5,
                "PotentialEnergyUsable": 10,
                "AvailableLand": 3,
                "Water": 5
            },
            outputs={
                "Dam": 1,
                "HousingWaste": 2
            },
            required={
                "SkilledLabor": 5,
            }
        ),
        TransformTemplate(
            name="BuildFactory",
            inputs={
                "MetallicAlloys": 8,
                "Timber": 8,
                "PotentialEnergyUsable": 8,
            },
            outputs={
                "Factories": 1,
                "HousingWaste": 1,
            },
            required={
                "SkilledLabor": 2,
                "Population": 5
            }
        ),
        TransformTemplate(
            name="RecycleElectronics",
            inputs={"ElectronicsWaste": 3, "PotentialEnergyUsable": 2},
            outputs={"MetallicAlloys": 1},
            required={"SkilledLabor": 1, "Factories": 1}
        ),
        TransformTemplate(
            name="CompostFood",
            inputs={
                "FoodWaste": 10
            },
            outputs={
                "FoodWaste": 8
            },
            required={
                "Population": 2
            }
        ),
    ]

    # 3. Initialize search
    initial_eu = compute_state_quality(world.get_country(your_country_name).resources, weights)
    initial_schedule = Schedule([], world, [initial_eu], [], 0)
    frontier = [(-initial_eu, next(counter), initial_schedule)]
    heapq.heapify(frontier)
    complete_schedules = []
    resource_weights = load_resource_weights()

    
    # 4. Search loop
    while frontier:
        _, _, schedule = heapq.heappop(frontier)

        if schedule.depth == depth_bound:
            complete_schedules.append((schedule.actions, schedule.eus, schedule.deltas))
            if track_resource_deltas:
                schedule_resource_deltas.append(schedule.deltas)
            continue

            
        successors = generate_successors(schedule.world, your_country_name, base_transforms, weights)

        for action_str, new_world, delta, delta_score in successors:
            new_country = new_world.get_country(your_country_name)
            new_eu = compute_state_quality(new_country.resources, weights)


            # Penalize transfers and score based on delta
            penalty = 0
            if "TRANSFER" in action_str:
                penalty = 10  # You can tune this
            score = delta_score - penalty

            print(f"{action_str} | ΔScore: {delta_score:.2f} | Raw EU: {new_eu:.2f} | Penalized Score: {score:.2f}")

            new_schedule = Schedule(
                actions=schedule.actions + [action_str],
                world=new_world,
                eus=schedule.eus + [schedule.eus[-1] + score],
                deltas=schedule.deltas + [delta],
                depth=schedule.depth + 1
            )

            total_score = new_eu 
            heapq.heappush(frontier, (-total_score, next(counter), new_schedule))


        if len(frontier) > frontier_max_size:
            heapq.heappop(frontier)

    # 5. Output results
    def score_schedule(actions, eus):
    # Total utility gain across all steps
        return sum(eus[i] - eus[i-1] for i in range(1, len(eus)))

    top_schedules = complete_schedules[:num_output_schedules]

    os.makedirs(os.path.dirname(output_schedule_filename), exist_ok=True)

    # Write .txt output
    with open(output_schedule_filename, "w") as f:
        for i, (actions, eus, _) in enumerate(top_schedules, 1):
            f.write(f"Schedule {i} (Final EU: {eus[-1]:.2f}):\n[")
            if len(actions) != len(eus) - 1:
                f.write("\n  ⚠️ WARNING: actions and EU lengths mismatched!\n")
            for j, (action, eu) in enumerate(zip(actions, eus[1:]), 1): 
                f.write(f"\n  Step {j}: {action} EU: {eu:.2f}")
            f.write("\n]\n\n")


    # Write JSON output
    schedule_log = [
        {
            "schedule_num": i + 1,
            "final_eu": eus[-1],
            "actions": [
                {"action": action, "eu": eu, "delta": delta}
                for action, eu, delta in zip(actions, eus[1:], deltas)
            ],
        }
        for i, (actions, eus, deltas) in enumerate(top_schedules)
    ]


    with open("output/schedule_log.json", "w") as json_f:
        json.dump(schedule_log, json_f, indent=2)
