import argparse
import sys

from tests.data_test.database_connection import DatabaseConn

print('=' * 40)
print('Mongo tools script launched!')
print('=' * 40)

print('Setting parsers...')
parser = argparse.ArgumentParser(description='Set of tools to make a backup/configuration of MongoDB.')
parser.add_argument('-bdir', '--backupdir', metavar='<OUTPUT_PATH>',
                    help='Set path to backup directory where to save the files.')
parser.add_argument('-hdir', '--homedir', metavar='<HOMEDIR_PATH>',
                    help='Set path to home directory where MongoDB is installed.')
parser.add_argument('-uP', '--update', default=0, const=1, action='store_const',
                    help='If provided value is not temporal, set -uP to update config.json with new values.')
args = sys.argv[1:]

args = ' '.join(args)
print('Reading arguments...')
values = parser.parse_args(args.split())

print('Connecting to MongoDB.')
d = DatabaseConn()

print('Host: %s' % d.host)

if values.backupdir:
    url = values.backupdir
    if values.update:
        print('Updating backup url with %s' % url)
        d.config_db(backupdir=url)
elif values.homedir and values.update:
    url = values.homedir
    print('Updating homedir url with %s' % url)
    d.config_db(homedir=url)
    sys.exit(0)
else:
    print('No arguments set! Continuing with backup...')
    url = None

print('Starting backup...')
d.backup_db(backup_url=url)
