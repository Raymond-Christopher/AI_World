# visualizations/resourcetracking.py
import matplotlib.pyplot as plt
import json
import csv
from collections import defaultdict
from typing import List, Dict

def plot_schedule_log(json_path, output_path, initial_resources_path):
    """
    Plots the per-step resource deltas from the schedule log JSON file.

    Args:
        json_path: Path to the schedule_log.json file.
        output_path: Path where to save the output PNG plot.
        top_n_resources: Number of most-changing resources to track.
    """
    with open(initial_resources_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        resources = set()
        for row in reader:
            resources.update(row.keys())
        resources.discard("Country")  # Remove country label if present

    # 2. Load schedule log
    with open(json_path, "r") as f:
        data = json.load(f)

    # 3. Select schedule to plot
    schedule = data[4]  # Schedule 5 (0-indexed)

    # 4. Collect deltas
    initial_values = {}
    with open(initial_resources_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Country"] == "Atlantis":  # Change if you want to make this dynamic
                for res in resources:
                    initial_values[res] = float(row[res])
                break

    time_series = {res: [initial_values.get(res, 0)] for res in resources}

    for action in schedule["actions"]:
        delta = action["delta"]
        for res in resources:
            change = delta.get(res, 0)
            time_series[res].append(time_series[res][-1] + change)

    # 5. Plot
    plt.figure(figsize=(10, 6))
    for res, values in time_series.items():
        plt.plot(range(len(values)), values, marker="o", label=res)

    plt.title("Schedule 5 Resource Deltas")
    plt.xlabel("Action Step")
    plt.ylabel("Delta (Cumulative)")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()