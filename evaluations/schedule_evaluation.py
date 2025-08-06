"""Functions to compute undiscounted and discounted rewards based on state
quality."""
import math
import copy
from itertools import product
from .state_quality import compute_state_quality


def compute_undiscounted_reward(country_before, country_after, weights: dict) -> float:
    """Computes the difference in state quality between two country states.

    :param country_before: A Country object (before schedule)
    :param country_after: A Country object (after schedule)
    :param weights: Dictionary of resource weights.
    :return: float representing Q_end - Q_start
    """
    q_start = compute_state_quality(country_before.resources, weights)
    q_end = compute_state_quality(country_after.resources, weights)
    return q_end - q_start


def compute_discounted_reward(
    start_country, end_country, steps: int, gamma: float, weights: dict
) -> float:
    """Calculates the discounted reward between two countries' resource states
    over a given number of steps.

    This function computes the difference in state quality between the starting and ending countries,
    discounted by a factor gamma raised to the power of the number of steps. The state quality is
    determined by the `compute_state_quality` function applied to each country's resources.
    :param start_country: The initial country object, expected to have a 'resources' attribute.
    :param end_country: The final country object, expected to have a 'resources' attribute.
    :param steps: The number of steps between the start and end states.
    :param gamma: The discount factor (default is 0.95).
    :return: The discounted reward as a float.
    """

    q_start = compute_state_quality(start_country.resources, weights)
    q_end = compute_state_quality(end_country.resources, weights)
    return (gamma**steps) * (q_end - q_start)

def logistic(x: float) -> float:
    """
    Computes the logistic sigmoid of x.

    :param x: Input value.
    :type x: float
    :return: Sigmoid output between 0 and 1.
    :rtype: float
    """
    return 1 / (1 + math.exp(-x))


def compute_expected_utility(schedule, world, country_name: str, weights: dict, gamma: float) -> float:
    """
    Computes the expected utility for a given schedule applied to a world state
    for a specific country.

    :param schedule: A list of (transform, country_name) pairs.
    :type schedule: list
    :param world: A World object containing Country objects.
    :type world: World
    :param country_name: The country to compute utility for.
    :type country_name: str
    :param weights: Dictionary of resource weights.
    :type weights: dict
    :param gamma: Discount factor.
    :type gamma: float
    :return: The expected utility value for the given schedule and country.
    :rtype: float
    """
    sim_world = copy.deepcopy(world)
    country_before = copy.deepcopy(sim_world.get_country(country_name))

    for transform, target_country in schedule:
        if sim_world.get_country(target_country).has_resources(transform.inputs):
            sim_world.get_country(target_country).apply_transform(
                transform.inputs, transform.outputs
        )


    country_after = sim_world.get_country(country_name)
    reward = compute_discounted_reward(
        country_before, country_after, steps=len(schedule), gamma=gamma, weights=weights
    )
    return logistic(reward)


def generate_schedules(transform_templates, country_name: str, max_length: int = 2, scales=[1, 3, 5]):
    """
    Generate all possible transform schedules for a specific country.

    :param transform_templates: List of base TransformTemplate objects.
    :param country_name: The name of the country these transforms apply to.
    :param max_length: Maximum number of transforms in a schedule.
    :param scales: List of scaling factors to apply to each template.
    :return: List of schedules, where each schedule is a list of (transform, country_name) pairs.
    """
    all_scaled_transforms = []

    for template in transform_templates:
        for scale in scales:
            scaled = template.scale(scale)
            all_scaled_transforms.append((scaled, country_name))

    all_schedules = []
    for length in range(1, max_length + 1):
        for combo in product(all_scaled_transforms, repeat=length):
            all_schedules.append(list(combo))

    return all_schedules

