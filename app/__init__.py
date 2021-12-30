import os
import connexion
from flask_cors import CORS
from flask_session import Session

from flask import session
from datetime import timedelta

from app.core.db import close_connection
from app.core.configs import Config
from app.core.error_handlers import (
    method_not_allowed_400,
    method_not_allowed_401,
    method_not_allowed_404,
    method_not_allowed_405,
)


def create_app():

    config = Config()

    try:
        OPENAPI_SPEC_PATH = os.environ["OPENAPI_SPEC_PATH"]
    except KeyError:
        OPENAPI_SPEC_PATH = "../openapi/"

    # try:
    #     MPT_DATABASE_PATH = os.environ["MPT_DATABASE_PATH"]
    # except KeyError:
    #     enter_db = input("Enter Database Path? (y/n): ")
    #     if enter_db == "y" or enter_db == "yes":
    #         MPT_DATABASE_PATH = input("MPT_DATABASE_PATH: ")
    #     else:
    #         print("ERROR: Database FILE NOT FOUND. 'MPT_DATABASE_PATH' not set")
    #         sys.exit(1)
    MPT_DATABASE_PATH = "/mnt/e/Projects/Mortgage_Payments_Tracker_API/app/database/"

    try:
        MPT_SECRET_KEY = os.environ["MPT_SECRET_KEY"]
    except KeyError:
        MPT_SECRET_KEY = "MyPassword"

    config.MPT_DATABASE_PATH = MPT_DATABASE_PATH

    app = connexion.FlaskApp(__name__, specification_dir=OPENAPI_SPEC_PATH)
    app.add_api("spec.yml", strict_validation=True)

    @app.app.teardown_appcontext
    def remove_session(exception):
        close_connection(exception)

    app.app.config["SECRET_KEY"] = MPT_SECRET_KEY
    app.app.config["SESSION_TYPE"] = "filesystem"
    app.app.config["SESSION_FILE_DIR"] = "/tmp/flask_cache"

    Session(app.app)
    CORS(app.app, supports_credentials=True)

    @app.app.before_request
    def before_request():
        session.permanent = True
        app.app.permanent_session_lifetime = timedelta(hours=6)

    app.add_error_handler(400, method_not_allowed_400)
    app.add_error_handler(401, method_not_allowed_401)
    app.add_error_handler(404, method_not_allowed_404)
    app.add_error_handler(405, method_not_allowed_405)

    return app.app
