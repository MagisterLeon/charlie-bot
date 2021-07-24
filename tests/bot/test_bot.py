import os

from bot.bot import ShroomMarketBot
from bot.contracts import ShroomMarketContract
from bot.inventory import Inventory
from bot.utils import to_bytes


def upload_inventory(utils, inventory_api_client, offer_id):
    offer_content = f"""
            genus: psilocybe
            mass: 10
            price: 100
            id: offer_1
            location: location_1
            sold: False
            """
    file_data = utils.build_file_data(offer_id, to_bytes(offer_content))
    inventory_api_client.post('/inventory', buffered=True, content_type='multipart/form-data', data=file_data)


def ask_for_offer(dai, shroom_market_contract, customer, seller, offer_id):
    dai.approve(shroom_market_contract, 100, {'from': customer})
    shroom_market_contract.ask(b'public_key', seller, to_bytes(offer_id), 100, {'from': customer})


def test_confirm_offer_and_mark_as_sold_when_handle_valid_offer_ask(shroom_market, inventory_api_client, dai,
                                                                    seller_account, customer_account,
                                                                    public_key, utils):
    # given
    offer_id = "offer_1"
    upload_inventory(utils, inventory_api_client, offer_id)
    ask_for_offer(dai, shroom_market, customer_account, seller_account, offer_id)

    contract = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")
    inventory = Inventory(os.environ["INVENTORY_PATH"])
    uut = ShroomMarketBot(contract, inventory)
    event = {
        "args": {
            "customer_pkey": public_key,
            "customer": customer_account,
            "seller": seller_account,
            "total": 100
        }
    }

    # when
    uut.handle_ask_event(event)

    # then
    assert dai.balanceOf(seller_account) == 100
    assert inventory.offers[offer_id].sold
    assert Inventory(os.environ["INVENTORY_PATH"]).offers[offer_id].sold


def test_ignore_sold_offers(shroom_market, inventory_api_client, dai,
                            seller_account, customer_account,
                            public_key, utils):
    # given
    offer_id = "offer_1"
    upload_inventory(utils, inventory_api_client, offer_id)
    ask_for_offer(dai, shroom_market, customer_account, seller_account, offer_id)

    contract = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")
    inventory = Inventory(os.environ["INVENTORY_PATH"])
    uut = ShroomMarketBot(contract, inventory)
    event = {
        "args": {
            "customer_pkey": public_key,
            "customer": customer_account,
            "seller": seller_account,
            "total": 100
        }
    }
    inventory.mark_offer_as_sold(offer_id)

    # when
    uut.handle_ask_event(event)

    # then
    assert dai.balanceOf(seller_account) == 0


def test_ignore_offers_with_different_id(shroom_market, inventory_api_client, dai,
                                         seller_account, customer_account,
                                         public_key, utils):
    # given
    offer_id = "offer_1"
    upload_inventory(utils, inventory_api_client, offer_id)
    ask_for_offer(dai, shroom_market, customer_account, seller_account, "offer_2")

    contract = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")
    inventory = Inventory(os.environ["INVENTORY_PATH"])
    uut = ShroomMarketBot(contract, inventory)
    event = {
        "args": {
            "customer_pkey": public_key,
            "customer": customer_account,
            "seller": seller_account,
            "total": 100
        }
    }

    # when
    uut.handle_ask_event(event)

    # then
    assert dai.balanceOf(seller_account) == 0
