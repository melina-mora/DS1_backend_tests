import argparse
import sys

from scripts.mongo_tools_script.mongo_connection import MongoDBConnection

print('=' * 40)
print('Mongo tools script launched!')
print('=' * 40)
d = MongoDBConnection()

print('> Setting parsers...')
parser = argparse.ArgumentParser(description='Set of tools to manipulate test data of local MongoDB.')
parser.add_argument('--backupdir', metavar='<OUTPUT_PATH>',
                    help='Set path to backup directory where to save the files.')
parser.add_argument('--homedir', metavar='<HOMEDIR_PATH>',
                    help='Set path to home directory where MongoDB is installed.')
parser.add_argument('-r', '--restore', default=0, const=1, action='store_const',
                    help='Set this flag to restore TestData files. Usually used after backup.')
parser.add_argument('-d', '--dump', default=0, const=1, action='store_const',
                    help='Set this flag to dump TestData files in backup directory configured in mongo_tools_config.json')

args = sys.argv[1:]

args = ' '.join(args)
print('> Reading arguments...')
values = parser.parse_args(args.split())

print('> Host: %s' % d.host)
print('> Database set: %s' % d.db)
print('> Collection set: %s' % d.coll)

if values.backupdir:
    d.config_db(backupdir=values.backupdir)
    sys.exit(0)

if values.dump:
    d.backup_db()
    sys.exit(0)

if values.homedir:
    d.config_db(homedir=values.homedir)
    sys.exit(0)

if values.restore:
    d.restore_db()
    sys.exit(0)

# region MONGODB INSTALLATION WIZARD

print('> No actions set...starting installation wizard...')
print('=' * 30)
print('!!!-------> Make sure MongoDB is installed <----------!!!')

not_configured = True

while not_configured:
    homedir = input('Path to MongoDB home directory: ')
    backupdir = input('Path where to store backupdir: ')

    print('These paths will be configured for homedir: %s, for backupdir: %s. ' % (homedir, backupdir))
    ok = input('Are these correct? (Y/N): ').upper()
    if ok == 'Y':
        d.config_db(backupdir=backupdir)
        d.config_db(homedir=homedir)
        not_configured = False
    else:
        print('Nothing was set.')
        sys.exit(0)

d.restore_db()

print('Installation wizard finished! For more uses of this script try the following commands: ')
parser.print_help()

#endregion
sys.exit(0)


