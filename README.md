# AI_World

## 🌍 Project Overview

This project implements a multi-method AI agent designed to reason about trade and development strategies for virtual countries in a simulated world. Each country manages a set of resources and makes decisions using a defined set of operations: **transforms** (internal development) and **transfers** (trades with other countries).

### Goals of Part 1

- Build a heuristic-based **State Quality function** to evaluate how "healthy" or "desirable" a country’s state is.
- Compute **Undiscounted** and **Discounted Rewards** from action sequences.
- Parse **country resources** and **resource weights** from CSV files.
- Parse **TRANSFORM templates** from text files.
- Simulate basic **resource transformations** and **inter-country transfers**.

---

## 🧠 Key Concepts

- **State Quality**: A heuristic score representing the well-being of a country based on its resources.
- **Transformations**: Convert one set of resources into another (e.g., Timber + Alloys → Housing).
- **Transfers**: Move resources between countries.
- **Discounted Reward**: Penalizes long schedules via a discount factor `γ`.
- **Expected Utility**: Combines Discounted Reward with estimated probability of success.

---

## 🗂 Project Structure

```
Development_mode/
├── main.py # Entry point for the simulation
├── README.md
├── pyproject.toml
├── parsers/
│ └── csv_parser.py # CSV parsing logic for country states and weights
├── models/
│ └── world_model.py # Country and World classes
├── transformations/
│ └── transformations.py # TransformTemplate class for resource transformations
├── evaluations/
│ ├── state_quality.py # Heuristic function for evaluating country state
│ └── schedule_evaluation.py # Computes rewards and utility based on quality
├── tests/
│ ├── test_csv_parser.py
│ ├── test_state_quality.py
│ └── ...
└── data/
├── resources.csv # Sample country resources
└── weights.csv # Resource weight configuration
```

---

## 🛠 Setup & Running

### Pre-requisites

- Python 3.8+
- No third-party dependencies (standard library only)

### Running the Simulation

```bash
cd Development_mode
python3 main.py
```

This will:

Print the initial state quality for each country.
Perform a resource transfer from one country to another.
Attempt a resource transformation (e.g., Housing).
Print the post-transform state and the computed discounted reward.

### Testing

To run unit tests:

```bash
cd Development_mode
python3 -m unittest discover tests
```

### Notes

All transformations must follow predefined templates.
All required resource types and waste resources are tracked.
The design supports expanding to Part 2 (planning agents and probabilistic success estimation).

### Author

Christopher Raymond
CS 5260 - Summer 2025
Vanderbilt University
