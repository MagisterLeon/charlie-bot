import pytest
from brownie import config, network

from inventory_client import create_app


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "UPLOAD_FOLDER": "./inventory"})
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
