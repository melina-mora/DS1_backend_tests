import pymongo
import os
import sys
import argparse
from datetime import datetime
from tools.json_tools import extract, update_json, string_to_json


class DatabaseConn:
	def __init__(self, db=None, coll=None):
		self._conn = pymongo.MongoClient("mongodb://localhost:27017/")  # Connection to local MongoDB
		self.db = self._conn[db] if db else None  # Connection to database
		self.coll = self.db[coll] if coll else None  # Connection to collection/table

	def backup_db(self):
		with open('config.json', 'r+', encoding='utf8') as f:
			config = f.read()
			
			home = extract(body=config, path='$.homedir')
			backup = extract(body=config, path='$.backupdir')

		if not os.path.isdir(home):
			print('The path specified for home does not exist')
			sys.exit()
		if not os.path.isdir(backup):
			print('The path specified for backup does not exist')
			sys.exit()

		os.system('cd %s' % home)
		os.system('mongodump --out=%s\\%s' % (backup, datetime.now().strftime('%Y%m%d_%H%M%S')))

	def config_db(self, args):
		with open('config.json', 'r', encoding='utf8') as f:
			data = f.read()
			data = string_to_json(data)

		data = update_json(body=data, values={'$.homedir': args})

		with open('config.json', 'w', encoding='utf8') as f:
			f.write(data)

	def config_args_parser(self):
		my_parser = argparse.ArgumentParser(description='Configure homedir for DB.')

		# Add the arguments
		my_parser.add_argument('-cdb',
		                       metavar='--configdb',
		                       type=str,
		                       help='path to MongoDB folder where DB is stored. If none specified, default will be used',
		                       action='store')

		# Execute the parse_args() method
		args, unknown = my_parser.parse_known_args(['-cdb', '--configdb'])

		if args.configdb or args.cdb:
			self.config_db(args)
		if unknown:
			print('Unrecognized arguments: %s' % unknown)


# C:\Program Files\MongoDB\Server\4.2\bin
print('------Starting database backup/config script-------\n')
print('> Available commands are:\n -h : For help \n --configdb <path> : for update homedir of MongoDB test data.')
print('\n > --backupdb : to generate a backup of current DB.')
config = DatabaseConn()
config.config_args_parser()
