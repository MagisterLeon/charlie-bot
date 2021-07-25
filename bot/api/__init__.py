import os

from flask import Flask, render_template

from bot.api import inventory
from bot.config import settings


def create_app(test_config=None):
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
    def upload_file():
        return render_template('index.html')

    app.register_blueprint(inventory.bp)

    return app
