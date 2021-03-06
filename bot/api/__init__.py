import os

from flask import Flask, render_template

from bot.api import inventory
from bot.config import settings
from bot.contracts import DaiContract
from bot.inventory import Inventory


def create_app(test_config=None):
    if not os.path.exists(settings.INVENTORY_PATH):
        os.makedirs(settings.INVENTORY_PATH)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        UPLOAD_FOLDER=settings.INVENTORY_PATH,
        MAX_CONTENT_PATH=500
    )

    if test_config is not None:
        app.config.update(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def home():
        offers = Inventory(settings.INVENTORY_PATH).offers.values()
        dai = DaiContract(settings.DAI_CONTRACT_ADDRESS, "/contracts/min_erc20_abi.json")
        return render_template('index.html', offers=offers, dai=dai.get_balance())

    app.register_blueprint(inventory.bp)

    return app
