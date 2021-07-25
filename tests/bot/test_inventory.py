from bot.config import settings
from bot.inventory import Inventory, Offer
from bot.utils import to_bytes


def upload_inventory(utils, inventory_api_client, offer: dict):
    offer_content = f"""
        genus: {offer['genus']}
        mass: {offer['mass']}
        price: {offer['price']}
        id: {offer['id']}
        location: {offer['location']}
        """
    file_data = utils.build_file_data(offer['id'], to_bytes(offer_content))
    inventory_api_client.post('/inventory', buffered=True, content_type='multipart/form-data', data=file_data)


def test_inventory_has_all_offers(inventory_api_client, utils):
    # given
    offer_1 = {
        "genus": "psilocybe",
        "mass": 10,
        "price": 100,
        "id": "8ec614b8-5e1b-4093-a4a6-777c44a2f4a2",
        "location": "location_1"
    }
    offer_2 = {
        "genus": "agaricus",
        "mass": 20,
        "price": 200,
        "id": "40a2a02a-1e90-4f96-a4ab-6e18d84fc52e",
        "location": "location_2"
    }
    upload_inventory(utils, inventory_api_client, offer_1)
    upload_inventory(utils, inventory_api_client, offer_2)
    uut = Inventory(settings.INVENTORY_PATH)

    # then
    assert uut.offers[offer_1['id']] == Offer(offer_1)
    assert uut.offers[offer_2['id']] == Offer(offer_2)


def test_mark_offer_as_sold(inventory_api_client, utils):
    # given
    offer_1 = {
        "genus": "psilocybe",
        "mass": 10,
        "price": 100,
        "id": "8ec614b8-5e1b-4093-a4a6-777c44a2f4a2",
        "location": "location_1"
    }
    upload_inventory(utils, inventory_api_client, offer_1)
    uut = Inventory(settings.INVENTORY_PATH)

    # when
    uut.mark_offer_as_sold(offer_1['id'])

    # then
    assert uut.offers[offer_1['id']].sold
    assert Inventory(settings.INVENTORY_PATH).offers[offer_1['id']].sold
