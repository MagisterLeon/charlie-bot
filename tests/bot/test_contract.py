import pytest
from Crypto.PublicKey import RSA

from bot.contracts import ShroomMarketContract
from bot.crypto import decrypt
from bot.events import AskEvent
from bot.inventory import Offer
from bot.utils import to_bytes


def upload_inventory(utils, inventory_api_client, offer_id):
    offer_content = f"""
        id: {offer_id}
        location: 50.654164, 16.512376
        """
    file_data = utils.build_file_data(offer_id, to_bytes(offer_content))
    inventory_api_client.post('/inventory', buffered=True, content_type='multipart/form-data', data=file_data)


def ask_for_offer(dai, shroom_market_contract, customer, seller, offer_id):
    dai.approve(shroom_market_contract, 100, {'from': customer})
    shroom_market_contract.ask(b'public_key', seller, to_bytes(offer_id), 100, {'from': customer})


@pytest.fixture
def ask(customer_account, public_key, seller_account):
    return AskEvent.from_values(public_key, customer_account, seller_account, 100)


def test_seller_should_receive_dai_when_confirm_order(shroom_market, inventory_api_client, dai, seller_account,
                                                      customer_account, utils, ask):
    # given
    offer_id = "offer_1"
    upload_inventory(utils, inventory_api_client, offer_id)
    ask_for_offer(dai, shroom_market, customer_account, seller_account, offer_id)

    uut = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")
    offer = Offer({
        "genus": "psilocybe",
        "mass": 10,
        "price": 100,
        "id": offer_id,
        "location": "50.654164, 16.512376"
    })

    # when
    uut.confirm_order(ask, offer)

    # then
    assert dai.balanceOf(seller_account) == 100


def test_customer_is_able_to_decrypt_secret_location_with_private_key(shroom_market, inventory_api_client, dai,
                                                                      seller_account, customer_account,
                                                                      utils, private_key, ask):
    # given
    offer_id = "offer_1"
    upload_inventory(utils, inventory_api_client, offer_id)
    ask_for_offer(dai, shroom_market, customer_account, seller_account, offer_id)

    uut = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")
    offer = Offer({
        "genus": "psilocybe",
        "mass": 10,
        "price": 100,
        "id": offer_id,
        "location": "50.654164, 16.512376"
    })

    # when
    uut.confirm_order(ask, offer)
    location = uut.contract.events.Confirm.createFilter(fromBlock="latest").get_all_entries()[0].args['location']

    # then
    decrypted_location = decrypt(location, RSA.importKey(private_key))
    assert decrypted_location == "50.654164, 16.512376"


def test_customer_is_not_able_to_decrypt_secret_location_with_another_private_key(shroom_market, inventory_api_client,
                                                                                  dai, seller_account, customer_account,
                                                                                  utils, ask,
                                                                                  another_private_key):
    # given
    offer_id = "offer_1"
    upload_inventory(utils, inventory_api_client, offer_id)
    ask_for_offer(dai, shroom_market, customer_account, seller_account, offer_id)

    uut = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")
    offer = Offer({
        "genus": "psilocybe",
        "mass": 10,
        "price": 100,
        "id": offer_id,
        "location": "50.654164, 16.512376"
    })

    # when
    uut.confirm_order(ask, offer)
    location = uut.contract.events.Confirm.createFilter(fromBlock="latest").get_all_entries()[0].args['location']

    # then
    with pytest.raises(ValueError) as info:
        decrypt(location, RSA.importKey(another_private_key))
        assert info == "Ciphertext with incorrect length."
