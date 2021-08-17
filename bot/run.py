import sys
from threading import Thread

from web3.types import LogReceipt

from bot import api
from bot.config import settings
from bot.contracts import ShroomMarketContract
from bot.events import EventListener, AskEvent
from bot.inventory import Inventory, Offer
from bot.utils import to_bytes


class ShroomMarketBot:

    def __init__(self, contract: ShroomMarketContract):
        self.contract = contract

    def __confirm_order(self, inventory: Inventory, offer: Offer, ask: AskEvent):
        print(f"Ask for the offer: {offer.id} is valid and bought by a customer, confirming the order",
              file=sys.stdout)
        self.contract.confirm_order(ask, offer)
        print(f"Marking the offer: {offer.id} as sold", file=sys.stdout)
        inventory.mark_offer_as_sold(offer.id)
        print(f"Offer: {offer.id} is confirmed and marked as sold", file=sys.stdout)

    def handle_ask_event(self, event: LogReceipt):
        ask = AskEvent(event)
        print(f"Handling ask event: [{ask.__str__()}]", file=sys.stdout)

        if ask.seller_address == settings.USER_ADDRESS:
            inventory = Inventory(settings.INVENTORY_PATH)
            print(f"Inventory loaded: {inventory.offers.keys()}", file=sys.stdout)
            for offer in inventory.offers.values():
                if offer.is_valid(ask.total) and self.contract.did_customer_buy_offer(ask, to_bytes(offer.id)):
                    self.__confirm_order(inventory, offer, ask)

    def run(self):
        ask_filter = self.contract.get_ask_events_filter()
        event_listener = EventListener(ask_filter, self.handle_ask_event, settings.EVENT_LISTENER_POLL_INTERVAL)
        print("Starting event listener", file=sys.stdout)
        event_listener.start()


def bot_run():
    shroom_market_contract = ShroomMarketContract(settings.SHROOM_MARKET_CONTRACT_ADDRESS,
                                                  "/contracts/shroom_market_abi.json")
    shroom_market_bot = ShroomMarketBot(shroom_market_contract)
    print("Running bot application", file=sys.stdout)
    shroom_market_bot.run()


if __name__ == "__main__":
    worker = Thread(target=bot_run, daemon=True)
    worker.start()
    print("Running API", file=sys.stdout)
    app = api.create_app()
    app.run(host='0.0.0.0')
