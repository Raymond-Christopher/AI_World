# main.py
from state_quality import compute_state_quality
from world_model import Country, World

def main():
    atlantis_resources = {
        "Population": 100,
        "Housing": 20,
        "HousingWaste": 3,
        "Electronics": 10,
        "ElectronicsWaste": 1,
        "MetallicAlloys": 5,
        "MetallicAlloysWaste": 2,
        "Timber": 40,
        "MetallicElements": 30,
        "Food": 60,
        "Water": 80,
        "FoodWaste": 4
    }

    atlantis = Country("Atlantis", atlantis_resources)
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
        "FoodWaste": 3
    }
    carpania = Country("Carpania", carpania_resources)

    world = World([atlantis, carpania])

    for country in world.all_countries():
        score = compute_state_quality(country.resources)
        print(f"State quality for {country.name}: {score:.2f}")

    transfer_items = [("Timber", 30), ("Food", 5), ("Water", 15)]
    world.transfer_resources("Atlantis", "Carpania", transfer_items)

    print("\n--- After Transfer ---")
    for country in world.all_countries():
        score = compute_state_quality(country.resources)
        print(f"{country.name}: {score:.2f}")

if __name__ == "__main__":
    main()

