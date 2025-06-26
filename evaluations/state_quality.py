"""Functions to compute state quality based on the country resources."""


def compute_state_quality(country_resources: dict, weights: dict) -> float:
    """Calculates the quality score of a state based on its available resources
    and population.

    The function computes a weighted sum of various resource quantities
    (such as Housing, Electronics, Food, etc.) and their respective
    wastes, then normalizes this sum by the population to provide a per-
    capita quality score. Negative weights are used for waste resources
    to penalize their presence.
    :param country_resources: dict A dictionary containing resource
        names as keys and their corresponding quantities as values. Must
        include the key "Population" for normalization.
    :return: float The computed state quality score per capita. Returns
        negative infinity if population is zero.
    """

    population = country_resources.get("Population", 0)
    if population == 0:
        return float("-inf")

    score = 0
    for res, weight in weights.items():
        amount = country_resources.get(res, 0)
        score += weight * amount

    return score / population
