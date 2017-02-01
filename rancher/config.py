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

    def is_valid(self):
        if not self.RANCHER_URL:
            return False
        if not self.RANCHER_ACCESS_KEY:
            return False
        if not self.RANCHER_SECRET_KEY:
            return False
        return True

    def not_valid(self):
        return not self.is_valid()
