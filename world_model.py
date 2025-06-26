class Country:
    """
    Represents a country with a set of resources and provides methods to query and modify them.

    Attributes:
        name (str): The name of the country.
        resources (dict): A dictionary mapping resource names to their quantities.

    Methods:
        get_resource(resource: str) -> int
            Returns the quantity of a specific resource.
            :param resource: The name of the resource to query.
            :return: The quantity of the specified resource, or 0 if not present.

        has_resources(required: dict) -> bool
            Checks if the country has at least the required amounts of each resource.
            :param required: A dictionary of required resources and their amounts.
            :return: True if all required resources are available in sufficient quantity, False otherwise.

        apply_transform(inputs: dict, outputs: dict)
            Consumes input resources and produces output resources, updating the country's resources.
            :param inputs: A dictionary of resources to consume and their amounts.
            :param outputs: A dictionary of resources to produce and their amounts.
            :raises ValueError: If the country lacks the required input resources.
    """
    def __init__(self, name: str, resources: dict):
        self.name = name
        self.resources = resources

    def get_resource(self, resource: str) -> int:
        return self.resources.get(resource, 0)

    def has_resources(self, required: dict) -> bool:
        return all(self.resources.get(k, 0) >= v for k, v in required.items())

    def apply_transform(self, inputs: dict, outputs: dict):
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
            Retrieves a country by name.
            :param name: The name of the country to retrieve.
            :type name: str
            :return: The Country object if found.
            :rtype: Country
        - all_countries() -> list:
            Returns a list of all Country objects in the world.
            :return: List of Country objects.
            :rtype: list
        - transfer_resources(sender_name: str, receiver_name: str, resource_list: list[tuple[str, int]]):
            Transfers resources from one country to another.
            :param sender_name: Name of the sending country.
            :type sender_name: str
            :param receiver_name: Name of the receiving country.
            :type receiver_name: str
            :param resource_list: List of (resource, amount) tuples to transfer.
            :type resource_list: list[tuple[str, int]]
            :raises ValueError: If sender or receiver is not found, or if sender lacks resources.
    """
    
    def __init__(self, countries: list):
        self.countries = {c.name: c for c in countries}

    def get_country(self, name: str) -> Country | None:
        country = self.countries.get(name)
        if country is None:
            raise ValueError(f"Country '{name}' not found.")
        return country

    def all_countries(self):
        return list(self.countries.values())

    def transfer_resources(
        self, sender_name: str, receiver_name: str, resource_list: list[tuple[str, int]]
    ):
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
            print(f"{sender.name} transferred {amount} {resource} to {receiver.name}.")
