import os
import pymongo
import sys

from tools.json_tools import string_to_json


class MongoDBConnection:
    def __init__(self, db=None, coll=None):
        self.host = 'mongodb://localhost:27017/'
        self.conn = pymongo.MongoClient(self.host)  # Connection to local MongoDB
        self.db = self.conn[db] if db else None  # Connection to database
        self.coll = self.db[coll] if coll else None  # Connection to collection/table
        url = os.path.join(os.path.dirname(__file__), 'mongo_tools_config.json')
        self._config_path = url if os.path.exists(url) else sys.exit(1)

        self.config = self.load_config()

    def load_config(self):
        with open(self._config_path, 'r+') as f:
            config = f.read()
            config = string_to_json(config)
        return config
