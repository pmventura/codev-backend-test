import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class Config(object):
    """
    Set Flask configuration vars from .env file
    """

    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
