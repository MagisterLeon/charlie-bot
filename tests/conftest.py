import os
import shutil
from io import BytesIO

import pytest
from Crypto.PublicKey import RSA
from brownie import config, network, accounts

from bot.config import settings
from inventory_api import create_app


class Utils:

    @staticmethod
    def build_file_data(offer_id: str, offer_content: bytes):
        return {
            'file': (BytesIO(offer_content), f"{offer_id}.yaml")
        }


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
def utils():
    return Utils


@pytest.fixture
def flask_app():
    app = create_app({"TESTING": True, "UPLOAD_FOLDER": settings.INVENTORY_PATH})
    yield app


@pytest.fixture
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
    with open(settings.ROOT_DIR + "/tests/resources/customer_public.pem", "rb") as fp:
        return RSA.importKey(fp.read())


@pytest.fixture(scope="module")
def private_key():
    with open(settings.ROOT_DIR + "/tests/resources/customer_private.pem", "rb") as fp:
        return RSA.importKey(fp.read())


@pytest.fixture(scope="module")
def another_private_key():
    with open(settings.ROOT_DIR + "/tests/resources/another_private.pem", "rb") as fp:
        return RSA.importKey(fp.read())
