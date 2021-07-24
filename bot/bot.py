import asyncio
import os

from web3.types import LogReceipt

from bot.contracts import ShroomMarketContract
from bot.events import EventListener, AskEvent
from bot.inventory import Inventory
from bot.utils import to_bytes


class ShroomMarketBot:

    def __init__(self, contract: ShroomMarketContract, inventory: Inventory):
        self.contract = contract
        self.inventory = inventory

    def handle_ask_event(self, event: LogReceipt):
        ask = AskEvent(event)
        if ask.seller_address == os.environ["USER_ADDRESS"]:
            for offer in self.inventory.offers.values():
                if offer.is_valid(ask.total) and self.contract.did_customer_buy_offer(ask, to_bytes(offer.id)):
                    self.contract.confirm_order(ask, offer)
                    self.inventory.mark_offer_as_sold(offer.id)

    def run(self):
        loop = asyncio.get_event_loop()
        try:
            ask_filter = self.contract.get_ask_events_filter()
            event_listener = EventListener(ask_filter, self.handle_ask_event, 2)
            loop.run_until_complete(
                asyncio.gather(event_listener.start())
            )
        finally:
            loop.close()


if __name__ == "__main__":
    shroom_market_contract = ShroomMarketContract(os.environ["SHROOM_MARKET_CONTRACT_ADDRESS"],
                                                  "/contracts/shroom_market_abi.json")
    inventory = Inventory(os.environ["INVENTORY_PATH"])
    bot = ShroomMarketBot(shroom_market_contract, inventory)
    bot.run()
