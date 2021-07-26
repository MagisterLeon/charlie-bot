import pytest
from Crypto.PublicKey import RSA

from bot.contracts import ShroomMarketContract
from bot.crypto import decrypt
from bot.events import AskEvent
from bot.inventory import Offer


@pytest.fixture
def ask(customer_account, public_key, seller_account):
    return AskEvent.from_values(public_key, customer_account, seller_account, 100)


@pytest.fixture
def setup(utils):
    utils.upload_offer_1_inventory()
    utils.customer_ask_for_offer("offer_1")


def test_seller_should_receive_dai_when_confirm_order(shroom_market, dai, seller_account, setup, ask, offer_1):
    # given
    uut = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")

    # when
    uut.confirm_order(ask, offer_1)

    # then
    assert dai.balanceOf(seller_account) == 100


def test_customer_is_able_to_decrypt_secret_location_with_private_key(shroom_market, setup, private_key, ask, offer_1):
    # given
    uut = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")

    # when
    uut.confirm_order(ask, offer_1)
    location = uut.contract.events.Confirm.createFilter(fromBlock="latest").get_all_entries()[0].args['location']

    # then
    decrypted_location = decrypt(location, RSA.importKey(private_key))
    assert decrypted_location == "50.654164, 16.512376"


def test_customer_is_not_able_to_decrypt_secret_location_with_another_private_key(shroom_market, setup, ask, offer_1,
                                                                                  another_private_key):
    # given
    uut = ShroomMarketContract(shroom_market.address, "/contracts/shroom_market_abi.json")

    # when
    uut.confirm_order(ask, offer_1)
    location = uut.contract.events.Confirm.createFilter(fromBlock="latest").get_all_entries()[0].args['location']

    # then
    with pytest.raises(ValueError) as info:
        decrypt(location, RSA.importKey(another_private_key))
        assert info == "Ciphertext with incorrect length."
