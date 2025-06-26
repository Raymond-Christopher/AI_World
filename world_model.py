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
        return self.countries.get(name)

    def all_countries(self):
        return list(self.countries.values())

    def transfer_resource(self, sender_name: str, receiver_name: str, resource: str, amount: int):
        sender = self.get_country(sender_name)
        receiver = self.get_country(receiver_name)

        if sender is None or receiver is None:
            raise ValueError("Sender or receiver country not found.")
        if sender.resources.get(resource, 0) < amount:
            raise ValueError(f"{sender.name} does not have enough of {resource} to transfer.")

        # Perform transfer
        sender.resources[resource] -= amount
        receiver.resources[resource] = receiver.resources.get(resource, 0) + amount
        print(f"{sender_name} transferred {amount} {resource} to {receiver_name}.")