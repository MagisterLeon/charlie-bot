import os
import shutil
from io import BytesIO

import pytest
from brownie import config, network, accounts

from bot.api import create_app
from bot.config import settings
from bot.crypto import import_rsa_key_bytes
from bot.inventory import Offer
from bot.utils import to_bytes


class Utils:

    def __init__(self, inventory_api_client, dai, shroom_market_contract, customer, seller, offer_1_dict):
        self.inventory_api_client = inventory_api_client
        self.dai = dai
        self.shroom_market_contract = shroom_market_contract
        self.customer = customer
        self.seller = seller
        self.offer_1_dict = offer_1_dict

    def build_file_data(self, offer_id: str, offer_content: bytes):
        return {
            'file': (BytesIO(offer_content), f"{offer_id}.yaml")
        }

    def upload_inventory(self, offer: dict):
        offer_content = f"""
            genus: {offer['genus']}
            mass: {offer['mass']}
            price: {offer['price']}
            id: {offer['id']}
            location: {offer['location']}
            """
        file_data = self.build_file_data(offer['id'], to_bytes(offer_content))
        self.inventory_api_client.post('/inventory', buffered=True, content_type='multipart/form-data', data=file_data)

    def upload_offer_1_inventory(self):
        self.upload_inventory(self.offer_1_dict)

    def customer_ask_for_offer(self, offer_id: str):
        self.dai.approve(self.shroom_market_contract, 100, {'from': self.customer})
        self.shroom_market_contract.ask(b'public_key', self.seller, to_bytes(offer_id), 100, {'from': self.customer})


@pytest.fixture(autouse=True)
def isolate(fn_isolation):
    # setup
    settings.HTTP_PROVIDER_URL = "http://127.0.0.1:8545"
    settings.INVENTORY_PATH = settings.ROOT_DIR + "/tests/inventory"
    os.mkdir(settings.INVENTORY_PATH)
    yield
    # teardown
    shutil.rmtree(settings.INVENTORY_PATH)


@pytest.fixture(scope="module")
def utils(inventory_api_client, dai, shroom_market, customer_account, seller_account, offer_1_dict):
    return Utils(inventory_api_client, dai, shroom_market, customer_account, seller_account, offer_1_dict)


@pytest.fixture(scope="module")
def flask_app():
    app = create_app({"TESTING": True, "UPLOAD_FOLDER": settings.INVENTORY_PATH})
    yield app


@pytest.fixture(scope="module")
def inventory_api_client(flask_app):
    return flask_app.test_client()


@pytest.fixture(scope="module")
def shroom_market(ShroomMarket):
    contract = ShroomMarket.deploy({'from': accounts[0]})
    settings.SHROOM_MARKET_CONTRACT_ADDRESS = contract.address
    return contract


@pytest.fixture(scope="module")
def dai(interface):
    return interface.ERC20(config['networks'][network.show_active()]['dai_address'])


@pytest.fixture(scope="module")
def seller_account():
    settings.USER_ADDRESS = accounts[1].address
    return accounts[1].address


@pytest.fixture(scope="module")
def customer_account():
    return config['networks'][network.show_active()]['customer_address']


@pytest.fixture(scope="module")
def public_key():
    return import_rsa_key_bytes("customer_public.pem")


@pytest.fixture(scope="module")
def private_key():
    return import_rsa_key_bytes("customer_private.pem")


@pytest.fixture(scope="module")
def another_private_key():
    return import_rsa_key_bytes("another_private.pem")


@pytest.fixture(scope="module")
def offer_1_dict():
    return {
        "genus": "psilocybe",
        "mass": 10,
        "price": 100,
        "id": "offer_1",
        "location": "50.654164, 16.512376"
    }


@pytest.fixture(scope="module")
def offer_1(offer_1_dict):
    return Offer(offer_1_dict)
