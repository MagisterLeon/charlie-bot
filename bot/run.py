import sys
from threading import Thread

from web3.types import LogReceipt

from bot import api
from bot.config import settings
from bot.contracts import ShroomMarketContract
from bot.events import EventListener, AskEvent
from bot.inventory import Inventory
from bot.utils import to_bytes


class ShroomMarketBot:

    def __init__(self, contract: ShroomMarketContract):
        self.contract = contract

    def handle_ask_event(self, event: LogReceipt):
        ask = AskEvent(event)
        if ask.seller_address == settings.USER_ADDRESS:
            inventory = Inventory(settings.INVENTORY_PATH)
            for offer in inventory.offers.values():
                if offer.is_valid(ask.total) and self.contract.did_customer_buy_offer(ask, to_bytes(offer.id)):
                    self.contract.confirm_order(ask, offer)
                    inventory.mark_offer_as_sold(offer.id)

    def run(self):
        ask_filter = self.contract.get_ask_events_filter()
        event_listener = EventListener(ask_filter, self.handle_ask_event, 2)
        event_listener.start()


def bot_run():
    print("Main: running bot application", file=sys.stdout)
    shroom_market_contract = ShroomMarketContract(settings.SHROOM_MARKET_CONTRACT_ADDRESS,
                                                  "/contracts/shroom_market_abi.json")
    shroom_market_bot = ShroomMarketBot(shroom_market_contract)
    shroom_market_bot.run()


if __name__ == "__main__":
    worker = Thread(target=bot_run, daemon=True)
    worker.start()
    print("Main: running API", file=sys.stdout)
    app = api.create_app()
    app.run()
