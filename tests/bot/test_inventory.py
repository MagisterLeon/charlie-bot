from bot.config import settings
from bot.inventory import Inventory, Offer


def test_inventory_has_all_offers(inventory_api_client, utils, offer_1):
    # given
    utils.upload_offer_1_inventory()
    offer_2 = {
        "genus": "agaricus",
        "mass": 20,
        "price": 200,
        "id": "offer_2",
        "location": "location_2"
    }
    utils.upload_inventory(offer_2)
    uut = Inventory(settings.INVENTORY_PATH)

    # then
    assert uut.offers["offer_1"] == offer_1
    assert uut.offers[offer_2['id']] == Offer(offer_2)


def test_mark_offer_as_sold(utils):
    # given
    offer_1 = "offer_1"
    utils.upload_offer_1_inventory()
    uut = Inventory(settings.INVENTORY_PATH)

    # when
    uut.mark_offer_as_sold(offer_1)

    # then
    assert uut.offers[offer_1].sold
    assert Inventory(settings.INVENTORY_PATH).offers[offer_1].sold
