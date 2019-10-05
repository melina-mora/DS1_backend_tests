import argparse
import sys

from tests.data_test.database_connection import DatabaseConn

print('=' * 40)
print('Mongo tools script launched!')
print('=' * 40)
d = DatabaseConn()

print('> Setting parsers...')
parser = argparse.ArgumentParser(description='Set of tools to manipulate test data of local MongoDB.')
parser.add_argument('--backupdir', metavar='<OUTPUT_PATH>',
                    help='Set path to backup directory where to save the files.')
parser.add_argument('--homedir', metavar='<HOMEDIR_PATH>',
                    help='Set path to home directory where MongoDB is installed.')
parser.add_argument('-r', '--restore', default=0, const=1, action='store_const',
                    help='Set this flag to restore TestData files. Usually used after backup.')
parser.add_argument('-d', '--dump', default=0, const=1, action='store_const',
                    help='Set this flag to dump TestData files in backup directory configured in config.json')

args = sys.argv[1:]

args = ' '.join(args)
print('> Reading arguments...')
values = parser.parse_args(args.split())

print('> Host: %s' % d.host)
print('> Database set: %s' % d.db)
print('> Collection set: %s' % d.coll)

if values.backupdir:
    print('> Updating backup url with %s' % values.backupdir)
    d.config_db(backupdir=values.backupdir)
    sys.exit(0)

if values.dump:
    print('> Starting backup...')
    d.backup_db()
    sys.exit(0)

if values.homedir:
    print('> Updating homedir url with %s' % values.homedir)
    d.config_db(homedir=values.homedir)
    sys.exit(0)

if values.restore:
    print('> Restoring local MongoDB files...')
    d.restore_db()
    sys.exit(0)

print('> No actions set...displaying help.')
parser.print_help()
sys.exit(0)


