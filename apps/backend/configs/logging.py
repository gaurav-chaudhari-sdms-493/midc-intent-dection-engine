import logging
from .settings import LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)
