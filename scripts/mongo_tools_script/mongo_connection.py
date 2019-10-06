import os
import subprocess
import sys
import glob
from datetime import datetime
from json import dumps

import pymongo

from tools.json_tools import extract, update_json, string_to_json


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

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output = os.path.join(backup, timestamp)
        os.mkdir(output)

        home = os.path.join(os.path.abspath(home), 'mongodump.exe')

        try:
            if os.path.exists(home):
                if os.path.exists(output):
                    print('> Making backup in: %s' % output)
                    subprocess.run('%s --out %s' % (home, output))
                    print('> Updating mongo_tools_config.json file last update.')
                    with open(self._config_path, 'w+') as f:
                        config = update_json(body=config, values={'$.lastupdate': timestamp})
                        config = dumps(config)
                        f.write(config)
                    print('> Backup done!')
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError as e:
            os.removedirs(output)
            if not os.path.exists(backup):
                os.mkdir(backup)
            print('Could not find paths. Backup directory was deleted.')
            print('Check paths: \n homedir: %s \n backupdir: %s' % (home, output))

    def restore_db(self, directory=None):
        with open(self._config_path, 'r+') as f:
            config = f.read()
            config = string_to_json(config)

            home = extract(body=config, path='$.homedir')
            backup = extract(body=config, path='$.backupdir')

        if not os.path.isdir(home):
            print('The path specified for home does not exist: %s' % home)
            sys.exit()
        if not os.path.isdir(backup):
            print('The path specified for backup does not exist: %s' % backup)
            sys.exit()

        all_subdirs = [d for d in os.listdir(backup) if os.path.isdir(backup)]
        latest_subdir = max(all_subdirs)

        home = os.path.join(os.path.abspath(home), 'mongorestore.exe')
        if directory:
            restore = os.path.join(backup, directory)
        else:
            restore = os.path.join(backup, latest_subdir)

        try:
            if os.path.exists(home):
                if os.path.exists(restore):
                    print('Restoring files from: %s' % restore)
                    subprocess.run('%s --dir=%s' % (home, restore))
                    print('> Updating mongo_tools_config.json file last update.')
                    with open(self._config_path, 'w+') as f:
                        config = update_json(body=config, values={'$.lastupdate': latest_subdir})
                        config = dumps(config)
                        f.write(config)
                    print('> Backup done!')
                else:
                    raise ValueError
            else:
                raise ValueError
        except Exception as e:
            print('Could not find make restore.')
            print('Check paths: \n homedir: %s \n restore from: %s' % (home, restore))
            print('Error thrown: \n %s' % e)

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