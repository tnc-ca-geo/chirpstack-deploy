"""
Backup ChirpStack data and push to S3.
"""
# standard library
from datetime import datetime
import gzip
import os
# third part
import sh


# (({database_name}, {database_owner}, {password}), ...)
DATABASES = ('chirpstack_ns', 'chirpstack_as')
# make sure that this user exists and has permissions to dump the above tables
DATABASE_USER = 'devuser'
DUMP_DIRECTORY = os.path.expanduser('~/chirpstack_dumps/')


def get_filename(db_name=None):
    """
    Create filename from db_name and date
    """
    part_1 = db_name or 'backup'
    part_2 = datetime.strftime(datetime.now(), '%Y_%m_%d')
    return '{}_{}.dump'.format(part_1, part_2)


def backup_db(database_name=None, directory='/tmp', filename=None):
    """
    Backup a database
    """
    # see https://medium.com/poka-techblog/5-different-ways-to-backup-your-postgresql-database-using-python-3f06cea4f51
    os.makedirs(directory, exist_ok=True)
    filename = filename or get_filename(database_name)
    pathname = os.path.abspath(os.path.join(directory, filename))
    if database_name:
        with open(pathname, 'wb') as fil:
            sh.pg_dump('-U', DATABASE_USER, database_name, '--create', _out=fil)
        return pathname


def main():
    print('\nBacking up ChirpStack databases:')
    for item in DATABASES:
        print ('-', item, end=' ')
        res = backup_db(item, DUMP_DIRECTORY)
        print('into', res)
    print('Done\n')


if __name__ == '__main__':
    main()
