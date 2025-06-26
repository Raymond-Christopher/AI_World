class Country:
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
    def __init__(self, countries: list):
        self.countries = {c.name: c for c in countries}

    def get_country(self, name: str) -> Country | None:
        country = self.countries.get(name)
        if country is None:
         raise ValueError(f"Country '{name}' not found.")
        return country

    def all_countries(self):
        return list(self.countries.values())

    def transfer_resources(self, sender_name: str, receiver_name: str, resource_list: list[tuple[str, int]]):
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

