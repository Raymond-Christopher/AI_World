from state_quality import compute_state_quality


def compute_undiscounted_reward(country_before, country_after) -> float:
    """
    Computes the difference in state quality between two country states.
    :param country_before: A Country object (before schedule)
    :param country_after: A Country object (after schedule)
    :return: float representing Q_end - Q_start
    """
    q_start = compute_state_quality(country_before.resources)
    q_end = compute_state_quality(country_after.resources)
    return q_end - q_start


def compute_discounted_reward(start_country, end_country, steps: int, gamma: float = 0.95) -> float:
    """
    Calculates the discounted reward between two countries' resource states over a given number of steps.
    This function computes the difference in state quality between the starting and ending countries,
    discounted by a factor gamma raised to the power of the number of steps. The state quality is
    determined by the `compute_state_quality` function applied to each country's resources.
    :param start_country: The initial country object, expected to have a 'resources' attribute.
    :param end_country: The final country object, expected to have a 'resources' attribute.
    :param steps: The number of steps between the start and end states.
    :param gamma: The discount factor (default is 0.95).
    :return: The discounted reward as a float.
    """

    q_start = compute_state_quality(start_country.resources)
    q_end = compute_state_quality(end_country.resources)
    return (gamma**steps) * (q_end - q_start)
