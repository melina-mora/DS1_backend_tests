from datetime import datetime
from json import dumps

import os
import pymongo
import sys

from tools.json_tools import extract, update_json, string_to_json


class DatabaseConn:
    def __init__(self, db=None, coll=None):
        self._conn = pymongo.MongoClient("mongodb://localhost:27017/")  # Connection to local MongoDB
        self.db = self._conn[db] if db else None  # Connection to database
        self.coll = self.db[coll] if coll else None  # Connection to collection/table
        url = os.path.join(os.path.dirname(__file__), 'config.json')
        self._config_path = url if os.path.exists(url) else sys.exit(1)

        self.config = self.load_config()

    def load_config(self):
        with open(self._config_path, 'r+') as f:
            config = f.read()
            config = string_to_json(config)
        return config

    def backup_db(self, backup_url=None):
        with open(self._config_path, 'r+') as f:
            config = f.read()
            config = string_to_json(config)

            home = extract(body=config, path='$.homedir')
            backup = extract(body=config, path='$.backupdir') if not backup_url else backup_url

        if not os.path.isdir(home):
            print('The path specified for home does not exist: %s' % home)
            sys.exit()
        if not os.path.isdir(backup):
            print('The path specified for backup does not exist: %s' % backup)
            sys.exit()

        output = os.path.join(backup, datetime.now().strftime('%Y%m%d_%H%M%S'))
        os.mkdir(output)

        home = os.path.join(os.path.abspath(home), 'mongodump.exe')
        home = home.replace(' ', '%20')
        try:
            os.system('%s --out %s' % (home, output))
        except Exception as e:
            os.removedirs(output)
            print('Could not find output path. Backup directory was deleted.')

    def config_db(self, **kwargs):
        with open(self._config_path, 'r') as f:
            data = f.read()
            data = string_to_json(data)

            json_values = dict()
        for k in kwargs.keys():
            json_values['$.%s' % k] = kwargs[k]

        data = update_json(body=data, values=json_values) if json_values else None

        if data:
            with open(self._config_path, 'w') as f:
                data = dumps(data)
                f.write(data)
