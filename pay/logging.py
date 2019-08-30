import logging.config

logging.config.fileConfig("logging.ini")
LOG = logging.getLogger(__name__)
