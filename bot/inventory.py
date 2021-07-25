from pathlib import Path
from typing import Dict

import yaml

from bot.config import settings
from bot.utils import format_decimals


class Offer:

    def __init__(self, offer: dict):
        self.id: str = offer['id']
        self.genus: str = offer['genus']
        self.mass: int = offer['mass']
        self.price: int = offer['price']
        self.location: str = offer['location']
        self.sold: bool = offer.get('sold', False)

    def __eq__(self, other):
        if not isinstance(other, Offer):
            return NotImplemented
        return (self.id == other.id and
                self.genus == other.genus and
                self.mass == other.mass and
                self.price == other.price and
                self.location == other.location and
                self.sold == other.sold
                )

    def __hash__(self):
        return hash((
            self.id,
            self.genus,
            self.mass,
            self.price,
            self.location,
            self.sold
        ))

    def __str__(self):
        return f"id: {self.id} | genus: {self.genus} | mass: {self.mass} " \
               f"| price: {format_decimals(self.price)} " \
               f"| location: {self.location} | sold: {self.sold} "

    def is_valid(self, price: int) -> bool:
        return not self.sold and price >= self.price


class Inventory:
    """
    Class responsible for loading offers stored in .yaml format to memory and execute operations on them
    """

    def __init__(self, inventory_path: str):
        self.offers: Dict[str, Offer] = {}
        for offer_path in Path(inventory_path).rglob("*.yaml"):
            offer = yaml.load(offer_path.open(), Loader=yaml.CLoader)
            self.offers[offer['id']] = Offer(offer)

    def mark_offer_as_sold(self, offer_id: str):
        with open(f"{settings.INVENTORY_PATH}/{offer_id}.yaml", 'w') as fp:
            offer = self.offers[offer_id]
            offer.sold = True
            yaml.dump(offer.__dict__, fp)
