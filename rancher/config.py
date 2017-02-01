from dotenv import load_dotenv, find_dotenv
from os import environ as env

class Config(object):
    def __init__(self, env_file=None):
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv(find_dotenv())

        self.RANCHER_URL = env.get('RANCHER_URL')
        self.RANCHER_ACCESS_KEY = env.get('RANCHER_ACCESS_KEY')
        self.RANCHER_SECRET_KEY = env.get('RANCHER_SECRET_KEY')
