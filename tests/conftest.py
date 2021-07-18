import os
import shutil

import pytest
from brownie import config, network

from inventory_client import create_app

INVENTORY_PATH = "inventory"


@pytest.fixture(autouse=True)
def isolate():
    # setup
    os.mkdir(INVENTORY_PATH)
    yield
    # teardown
    shutil.rmtree(INVENTORY_PATH)


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "UPLOAD_FOLDER": INVENTORY_PATH})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def get_charlie_account():
    return config['networks'][network.show_active()]['charlie_address']


@pytest.fixture(scope="module")
def get_customer_account():
    return config['networks'][network.show_active()]['customer_address']
