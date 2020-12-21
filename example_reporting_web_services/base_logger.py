import logging
from logging.config import fileConfig
from os import path

# init logging

log_file_path = path.join(path.dirname(path.abspath(__file__)), "config/logging.cfg")
fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)
