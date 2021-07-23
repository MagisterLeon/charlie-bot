import os
import shutil
from io import BytesIO

import pytest
from Crypto.PublicKey import RSA
from brownie import config, network, accounts

from inventory_api import create_app


class Utils:

    @staticmethod
    def build_file_data(offer_id: str, offer_content: bytes):
        return {
            'file': (BytesIO(offer_content), f"{offer_id}.yaml")
        }


@pytest.fixture(autouse=True)
def isolate():
    # setup
    os.environ["INVENTORY_PATH"] = "/tmp/inventory"
    os.mkdir(os.environ["INVENTORY_PATH"])
    yield
    # teardown
    shutil.rmtree(os.environ["INVENTORY_PATH"])


@pytest.fixture(scope="module")
def utils():
    return Utils


@pytest.fixture
def flask_app():
    app = create_app({"TESTING": True, "UPLOAD_FOLDER": os.environ["INVENTORY_PATH"]})
    yield app


@pytest.fixture
def inventory_api_client(flask_app):
    return flask_app.test_client()


@pytest.fixture(scope="module")
def shroom_market(ShroomMarket):
    contract = ShroomMarket.deploy({'from': accounts[0]})
    os.environ["SHROOM_MARKET_CONTRACT_ADDRESS"] = contract.address
    return contract


@pytest.fixture(scope="module")
def dai(interface):
    return interface.ERC20(config['networks'][network.show_active()]['dai_address'])


@pytest.fixture(scope="module")
def seller_account():
    return accounts[0].address


@pytest.fixture(scope="module")
def customer_account():
    return config['networks'][network.show_active()]['customer_address']


@pytest.fixture(scope="module")
def public_key():
    with open("../resources/public.pem", "rb") as fp:
        return RSA.importKey(fp.read())


@pytest.fixture(scope="module")
def private_key():
    with open("../resources/private.pem", "rb") as fp:
        return RSA.importKey(fp.read())
