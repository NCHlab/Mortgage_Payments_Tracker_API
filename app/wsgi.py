import logging

from app import create_app

logger = logging.getLogger(__name__)

application = app = create_app()

logger.info("MPT API Started")
