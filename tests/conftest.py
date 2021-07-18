import os
import shutil
from io import BytesIO

import pytest
from brownie import config, network, accounts

from inventory_api import create_app

INVENTORY_PATH = "inventory"


class Utils:

    @staticmethod
    def build_file_data(offer_id: str):
        return {
            'file': (BytesIO(b'file content'), f"{offer_id}.yaml")
        }


@pytest.fixture(autouse=True)
def isolate():
    # setup
    os.mkdir(INVENTORY_PATH)
    yield
    # teardown
    shutil.rmtree(INVENTORY_PATH)


@pytest.fixture(scope="module")
def utils():
    return Utils


@pytest.fixture
def flask_app():
    app = create_app({"TESTING": True, "UPLOAD_FOLDER": INVENTORY_PATH})
    yield app


@pytest.fixture
def inventory_api_client(flask_app):
    return flask_app.test_client()


@pytest.fixture(scope="module")
def shroom_market(ShroomMarket):
    return ShroomMarket.deploy({'from': accounts[0]})


@pytest.fixture(scope="module")
def dai(interface):
    return interface.ERC20(config['networks'][network.show_active()]['dai_address'])


@pytest.fixture(scope="module")
def charlie_account():
    return config['networks'][network.show_active()]['charlie_address']


@pytest.fixture(scope="module")
def customer_account():
    return config['networks'][network.show_active()]['customer_address']
