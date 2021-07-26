import pytest

from bot.config import settings
from bot.contracts import ShroomMarketContract
from bot.inventory import Inventory
from bot.run import ShroomMarketBot


@pytest.fixture
def ask_event(public_key, customer_account, seller_account):
    return {
        "args": {
            "customer_pubk": public_key,
            "customer": customer_account,
            "seller": seller_account,
            "total": 100
        }
    }


@pytest.fixture
def setup(utils):
    utils.upload_offer_1_inventory()
    utils.customer_ask_for_offer("offer_1")


def test_confirm_offer_and_mark_as_sold_when_handle_valid_offer_ask(shroom_market, dai, seller_account, ask_event,
                                                                    setup):
    # given
    contract = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")
    uut = ShroomMarketBot(contract)

    # when
    uut.handle_ask_event(ask_event)

    # then
    assert dai.balanceOf(seller_account) == 100
    assert Inventory(settings.INVENTORY_PATH).offers["offer_1"].sold


def test_ignore_sold_offers(shroom_market, dai, seller_account, ask_event, setup):
    # given
    contract = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")
    uut = ShroomMarketBot(contract)
    inventory = Inventory(settings.INVENTORY_PATH)
    inventory.mark_offer_as_sold("offer_1")

    # when
    uut.handle_ask_event(ask_event)

    # then
    assert dai.balanceOf(seller_account) == 0


def test_ignore_offers_with_different_id(shroom_market, dai, seller_account, utils, ask_event):
    # given
    utils.upload_offer_1_inventory()
    utils.customer_ask_for_offer("offer_2")
    contract = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")
    uut = ShroomMarketBot(contract)

    # when
    uut.handle_ask_event(ask_event)

    # then
    assert dai.balanceOf(seller_account) == 0
