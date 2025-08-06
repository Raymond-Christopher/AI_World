"""Defines the Country and World classes for simulating resource management and
transfers."""

from typing import List, Tuple


class Country:
    """Represents a country with a set of resources and provides methods to
    query and modify them.

    Attributes:
        name (str): The name of the country.
        resources (dict): A dictionary mapping resource names to their quantities.

    Methods:
        get_resource(resource: str) -> int
        has_resources(required: dict) -> bool
        apply_transform(inputs: dict, outputs: dict)

    """

    def __init__(self, name: str, resources: dict):
        """Initialize a Country with a name and resource dictionary.

        :param name: The country's name.
        :param resources: A dictionary of resource names to quantities.
        """
        self.name = name
        self.resources = resources

    def get_resource(self, resource: str) -> int:
        """Get the quantity of a specific resource.

        :param resource: The name of the resource to query.
        :return: Quantity of the resource, or 0 if not present.
        """
        return self.resources.get(resource, 0)

    def has_resources(self, required: dict) -> bool:
        """Check if the country has at least the required amounts of each
        resource.

        :param required: A dictionary of required resources and amounts.
        :return: True if all are available, False otherwise.
        """

        return all(self.resources.get(k, 0) >= v for k, v in required.items())

    def apply_transform(self, inputs: dict, outputs: dict):
        """Apply a transformation by consuming inputs and producing outputs.

        :param inputs: Dictionary of resource inputs to consume.
        :param outputs: Dictionary of resource outputs to produce.
        :raises ValueError: If the country lacks the required input
            resources.
        """
        if not self.has_resources(inputs):
            raise ValueError(f"{self.name} lacks required resources: {inputs}")
        for r, amt in inputs.items():
            self.resources[r] -= amt
        for r, amt in outputs.items():
            self.resources[r] = self.resources.get(r, 0) + amt


class World:
    """
    Represents a world containing multiple countries and provides methods to interact with them.
    This class manages a collection of Country objects, allowing retrieval, listing, and resource transfers between countries.
    Example:
        class Country:
            def __init__(self, name, resources):
                self.name = name
                self.resources = resources
        countries = [
            Country("CountryA", {"gold": 100, "oil": 50}),
            Country("CountryB", {"gold": 80, "oil": 60}),
        ]
        world = World(countries)
        world.transfer_resources("CountryA", "CountryB", [("gold", 10)])
    :param countries: List of Country objects to initialize the world with.
    :type countries: list
    :raises ValueError: If a requested country is not found or if a resource transfer is invalid.
    :methods:
        - get_country(name: str) -> Country | None:
        - all_countries() -> list:
        - transfer_resources(sender_name: str, receiver_name: str, resource_list: list[tuple[str, int]]):

    """

    def __init__(self, countries: List):
        """Initialize the world with a list of Country objects.

        :param countries: List of Country instances.
        """
        self.countries = {c.name: c for c in countries}

    def get_country(self, name: str) -> Country:
        """Retrieve a country by name.

        :param name: Name of the country.
        :return: Country object.
        :raises ValueError: If country is not found.
        """
        country = self.countries.get(name)
        if country is None:
            raise ValueError(f"Country '{name}' not found.")
        return country

    def all_countries(self):
        """Return a list of all countries in the world.

        :return: List of Country objects.
        """
        return list(self.countries.values())

    def transfer_resources(
        self, sender_name: str, receiver_name: str, resource_list: List[Tuple[str, int]]
    ):
        """Transfer resources from one country to another.

        :param sender_name: Name of the country sending resources.
        :param receiver_name: Name of the country receiving resources.
        :param resource_list: List of (resource, amount) tuples.
        :raises ValueError: If a country is missing or lacks resources.
        """
        sender = self.get_country(sender_name)
        receiver = self.get_country(receiver_name)

        if sender is None or receiver is None:
            raise ValueError("Sender or receiver country not found.")

        for resource, amount in resource_list:
            if sender.resources.get(resource, 0) < amount:
                raise ValueError(
                    f"{sender.name} does not have enough of {resource} to transfer. "
                    f"Has {sender.resources.get(resource, 0)}, needs {amount}."
                )

        for resource, amount in resource_list:
            sender.resources[resource] -= amount
            receiver.resources[resource] = receiver.resources.get(resource, 0) + amount
            # print(f"{sender.name} transferred {amount} {resource} to {receiver.name}.")
    
    def clone(self):
        """Return a deep copy of the world state (used for search branching)."""
        cloned_countries = [
            Country(c.name, c.resources.copy()) for c in self.all_countries()
        ]
        return World(cloned_countries)
