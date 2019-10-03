import argparse
import sys
from tests.data_test.database_connection import DatabaseConn
from tools.json_tools import extract

print('=' * 40)
print('Mongo tools script launched!')
print('=' * 40)
d = DatabaseConn()

print('> Setting parsers...')
parser = argparse.ArgumentParser(description='Set of tools to manipulate test data of local MongoDB.')
parser.add_argument('-bdir', '--backupdir', metavar='<OUTPUT_PATH>',
                    help='Set path to backup directory where to save the files.')
parser.add_argument('-hdir', '--homedir', metavar='<HOMEDIR_PATH>',
                    help='Set path to home directory where MongoDB is installed.')
parser.add_argument('-uP', '--update', default=0, const=1, action='store_const',
                    help='If provided path is permanent, set -uP to update config.json with new path.')
parser.add_argument('-r', '--restore', default=0, const=1, action='store_const',
                    help='Set this flag to restore TestData files. Usually used after backup.')

args = sys.argv[1:]

args = ' '.join(args)
print('> Reading arguments...')
values = parser.parse_args(args.split())



print('> Host: %s' % d.host)
print('> Database set: %s' % d.db)
print('> Collection set: %s' % d.coll)

if values.backupdir:
    url = values.backupdir
    if values.update:
        print('> Updating backup url with %s' % url)
        d.config_db(backupdir=url)
    else:
        print('> Starting backup...')
        d.backup_db(backup_url=url)

if values.homedir and values.update:
    url = values.homedir
    print('> Updating homedir url with %s' % url)
    d.config_db(homedir=url)
elif values.homedir:
    print('> Must set flag -uP to update path to home directory...')
    sys.exit(1)

if values.update and not values.homedir and not values.backupdir:
    url=extract(body=d.config, path='$.backupdir')
    print('> Starting backup...')
    d.backup_db(backup_url=url)
    sys.exit(0)

if values.restore:
    print('> Restoring local MongoDB files...')
    d.restore_db()
    sys.exit(0)

print('> No actions set...')
parser.print_help()
sys.exit(0)


