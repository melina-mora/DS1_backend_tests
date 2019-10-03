import argparse
import sys

from data_test.database_connection import DatabaseConn

parser = argparse.ArgumentParser(description='Set of tools to make a backup/configuration of MongoDB.')
parser.add_argument('-bdir', '--backupdir', metavar='<OUTPUT_PATH>',
                    help='Set path to backup directory where to save the files.')
parser.add_argument('-hdir', '--homedir', metavar='<HOMEDIR_PATH>',
                    help='Set path to home directory where MongoDB is installed.')
parser.add_argument('-uP', '--update', default=0, const=1, action='store_const',
                    help='For backup, update config.json with new values.')
args = sys.argv[1:]

args = ' '.join(args)
values = parser.parse_args(args.split())
d = DatabaseConn()

if values.backupdir:
    url = values.backupdir
    if values.update:
        d.config_db(backupdir=url)
elif values.homedir and values.update:
    url = values.homedir
    d.config_db(homedir=url)
    sys.exit(0)
else:
    url = None

d.backup_db(backup_url=url)
