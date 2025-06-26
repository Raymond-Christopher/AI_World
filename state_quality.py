def compute_state_quality(country_resources):
    weights = {
        "Housing": 3.0,
        "HousingWaste": -2.0,
        "Electronics": 4.0,
        "ElectronicsWaste": -2.0,
        "MetallicAlloys": 2.0,
        "MetallicAlloysWaste": -1.5,
        "Timber": 1.0,
        "MetallicElements": 1.5,
        "Food": 3.0,
        "Water": 2.0,
        "FoodWaste": -1.5,
    }

    population = country_resources.get("Population", 0)
    if population == 0:
        return float("-inf")

    score = 0
    for res, weight in weights.items():
        amount = country_resources.get(res, 0)
        score += weight * amount

    return score / population
