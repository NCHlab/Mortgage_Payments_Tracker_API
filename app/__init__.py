import os, sys
import logging
import connexion

from flask import session
from flask_cors import CORS
from flask_session import Session

from datetime import timedelta

from app.core.db import close_connection
from app.core.configs import Config
from app.core.error_handlers import (
    method_not_allowed_400,
    method_not_allowed_401,
    method_not_allowed_404,
    method_not_allowed_405,
)
from app.core import log


def create_app():

    config = Config()

    logger = logging.getLogger(__name__)

    try:
        MPT_LOG_LEVEL = os.environ["MPT_LOG_LEVEL"]
    except:
        MPT_LOG_LEVEL = "INFO"

    log_level = log.convert_log_setting(MPT_LOG_LEVEL)
    log.setup_logger(logger, log_level)

    logger.info("Logger Setup", extra={"base_log_level": MPT_LOG_LEVEL})

    try:
        OPENAPI_SPEC_PATH = os.environ["OPENAPI_SPEC_PATH"]
    except KeyError:
        logger.error("OPEN API Spec not found, 'OPENAPI_SPEC_PATH' not set.")
        sys.exit(1)

    try:
        MPT_DATABASE_PATH = os.environ["MPT_DATABASE_PATH"]
    except KeyError:
        logger.error("Database FILE NOT FOUND. 'MPT_DATABASE_PATH' not set")
        sys.exit(1)

    try:
        MPT_SECRET_KEY = os.environ["MPT_SECRET_KEY"]
    except KeyError:
        logger.error("Session Secret Key not found, 'MPT_SECRET_KEY' not set.")
        sys.exit(1)

    config.MPT_DATABASE_PATH = MPT_DATABASE_PATH

    app = connexion.FlaskApp(__name__, specification_dir=OPENAPI_SPEC_PATH)
    app.add_api("spec.yml", strict_validation=True)

    @app.app.teardown_appcontext
    def remove_session(exception):
        close_connection(exception)

    app.app.config["SECRET_KEY"] = MPT_SECRET_KEY
    app.app.config["SESSION_TYPE"] = "filesystem"
    app.app.config["SESSION_FILE_DIR"] = "/tmp/mpt_flask_cache"
    app.app.config["SESSION_COOKIE_SAMESITE"] = None
    app.app.config["SESSION_COOKIE_SECURE"] = True

    Session(app.app)
    CORS(app.app, supports_credentials=True)

    # Session Token Lifetime
    @app.app.before_request
    def before_request():
        session.permanent = True
        app.app.permanent_session_lifetime = timedelta(hours=6)

    app.add_error_handler(400, method_not_allowed_400)
    app.add_error_handler(401, method_not_allowed_401)
    app.add_error_handler(404, method_not_allowed_404)
    app.add_error_handler(405, method_not_allowed_405)

    return app.app
