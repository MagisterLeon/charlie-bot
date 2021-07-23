from pathlib import Path

import yaml


class Inventory:

    def __init__(self, inventory_path: str):
        self.offers = {}
        for offer_path in Path(inventory_path).rglob("*.yaml"):
            offer = yaml.load(offer_path.open(), Loader=yaml.CLoader)
            self.offers[offer['id']] = offer
