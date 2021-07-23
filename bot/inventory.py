import os
from pathlib import Path

import yaml


class Inventory:

    def __init__(self, inventory_path: str):
        self.offers = {}
        for offer_path in Path(inventory_path).rglob("*.yaml"):
            offer = yaml.load(offer_path.open(), Loader=yaml.CLoader)
            self.offers[offer['id']] = offer

    def mark_offer_as_sold(self, offer_id: str):
        inventory_path = os.environ["INVENTORY_PATH"]
        with open(f"{inventory_path}/{offer_id}.yaml", 'w') as fp:
            offer = self.offers[offer_id]
            offer['sold'] = True
            yaml.dump(offer, fp)
