# visualizations/plot_schedule.py

import json
import matplotlib.pyplot as plt
import os

def plot_schedule_log(json_path: str, output_path: str):
    with open(json_path) as f:
        data = json.load(f)

    plt.figure(figsize=(10, 6))

    for entry in data:
        steps = list(range(1, len(entry["actions"]) + 1))
        eus = [a["eu"] for a in entry["actions"]]
        label = f"Schedule {entry['schedule_num']}"
        plt.plot(steps, eus, marker="o", label=label)

    plt.title("Expected Utility Progression per Schedule")
    plt.xlabel("Action Step")
    plt.ylabel("Expected Utility (EU)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
