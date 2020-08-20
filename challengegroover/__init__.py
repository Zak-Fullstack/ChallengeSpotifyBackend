from flask import Flask, redirect, url_for
import logging
import logging.handlers
import os

from .routes import *
from .spotify_fetch import SpotifyFetch
from .schedule import should_update

def create_app():
    # config
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="ui/templates",
        static_folder="ui/static",
    )
    app.config.from_pyfile("config.py")

    # logging
    handler = logging.handlers.RotatingFileHandler(
        app.config["LOG_FILE"], maxBytes=app.config["LOG_SIZE"]
    )
    handler.setLevel(app.config["LOG_LEVEL"])
    handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(pathname)s at %(lineno)s]: %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
    )
    app.logger.addHandler(handler)

    # update the database every day
    filename = SpotifyFetch().DBNAME
    if (os.path.exists(filename) == False) or should_update(filename):
        SpotifyFetch().store_new_releases_in_db()

    # routes
    with app.app_context():
        from .routes import auth, root, api

        app.register_blueprint(root)
        app.register_blueprint(auth)
        app.register_blueprint(api)

    return app
