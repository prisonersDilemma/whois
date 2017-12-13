#!/usr/bin/env python3.6
"""Create an sqlite3 database, table, or insert records."""
from logging import getLogger
from os.path import basename, splitext
from sqlite3 import connect

logger = getLogger(__name__)


def conn_and_exec(**kwargs):
    """Connect to the database and execute an SQL *stmt* if any."""
    with connect(kwargs.get('file')) as conn:
        c = conn.cursor()                            # Create a cursor object
        stmt = kwargs.get('stmt')
        vals = kwargs.get('vals', '')                # Empty string if not present
        c.execute(stmt, vals)                        # Execute the SQL statement
        conn.commit()                                # Saves changes.


def create_database(fpath):
    with connect(fpath) as conn:
        return


def create_table(dbpath, keys, name=None):
    name = name if name else gettablename(dbpath)
    cols = ' text, '.join(keys) + ' text'
    sql_stmt = 'CREATE TABLE IF NOT EXISTS ' + name + ' (' + cols + ')'
    conn_and_exec(file=dbpath, stmt=sql_stmt)
    # Put this in database.
    logger.info(f'table {name} created if it does not exist.')


def insert_record(dbpath, values, name=None):
    """Insert a list of values into the specified table at 'path2db'

    NULL gets inserted by default by SQL if a value is absent a field/column.
    Fields/columns can be specified by including a tuple of only those with
    values after the table name.  In this case, if fields is not given, an
    empty string is inserted into the sql statement, and SQL makes the
    assumption that values are provided for all fields.
    """
    name = name if name else gettablename(dbpath)
    n = len(values) # Get from table, or still could cause an error.
    sql_stmt = f' {name} '.join(['INSERT INTO',  'VALUES'])
    sql_stmt = ' '.join([sql_stmt, ('?,'*(n-1) + '?').join(['(', ')'])])
    conn_and_exec(file=dbpath, stmt=sql_stmt, vals=values)


    #fields = ', '.join(fields).join(['(', ')']) if fields is not None else ''
    #c.execute(' '.join(['insert into', table, fields, 'values', str(tuple(values))]))
    #return conn_and_exec(filepath, ' '.join(['insert into', table_name, 'values', str(tuple(values))]))


#===============================================================================
#def select_all_containing(database_file, table_name, col, vals):
#
#    # Short-cut to put the string in a tuple, by following the item with a comma.
#    #sql_stmt = ' '.join(['select * from', table, 'where', field, 'like ?'])
#    #
#
#    #name = get_table_name(database_file)
#    #val = ('%'.join(vals).join(['%', '%']), )
#
#    #search_pattern = ('%'.join(search_strings).join(['%', '%']), )
#    #return c.fetchall()
#
#    sql_stmt = ' '.join(['select * from', table_name, 'where', field, 'like ?'])
#    return conn_and_exec(database_file, sql_stmt, val, True)


#def gettablename(dbpath):
#    """Return the basename of the database filepath. Assumes the table is of the same name."""
#    return splitext(basename(dbpath))[0]


#def get_tables(path_to_database):
#    """Returns a list of all the tabls in an sqlite3 database.
#
#    Slowest of all the ways to get the tables; using the dict is much, much
#    faster!  Alternatively, the pandas module could be used.
#
#
#    Note:  c.fetchall() is a list of tuples:  [(table1, ), (table2, )]
#    """
#    with connect(path_to_database) as conn:
#        c = conn.cursor()
#        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
#        return [t[0] for t in c.fetchall()]



#def get_fields(filepath, table_name):
#    """Return a list of fields in a table of a database.
#    Could make this similar to other functions and called by conn_and_exec().
#    Might not even need this at all.
#
#    Including table_name param in case there are multiple tables, rather than
#    assuming table_name will always be the file basename.
#
#    Returns a cursor object (generator) of tuples for each column that look
#    something like this: (0, 'file', 'text', 0, None, 0)
#    sql statement:  "pragma table_info(jeffsdb20170405)"
#
#    c.fetchall() produces something like this: (0, 'file', 'text', 0, None, 0)
#    This is the sqlite3 statement:  "pragma table_info(jeffsdb20170405)"
#    """
#    with connect(filepath) as conn:
#        c = conn.cursor()
#        c.execute(''.join(["pragma table_info(", table_name, ")"]))
#    return [field[1] for field in c.fetchall()]



#def insert_into_tbl2(path2db, table, values, fields=None):
#    """Insert a list of values into the specified table at 'path2db'
#
#    NULL gets inserted by default by SQL if a value is absent a field/column.
#    Fields/columns can be specified by including a tuple of only those with
#    values after the table name.  In this case, if fields is not given, an
#    empty string is inserted into the sql statement, and SQL makes the
#    assumption that values are provided for all fields.
#    """
#    fields = ', '.join(fields).join(['(', ')']) if fields is not None else ''
#    with connect(path2db) as conn:
#        c = conn.cursor()
#        c.execute(' '.join(['insert into', table, fields, 'values', str(tuple(values))]))
#        conn.commit()



#def insert_into_tbl3(values, schema, path2db, table):
#    """This is an example of using the executescript() method to build the table."""
#    with connect(path2db) as conn:
#        conn.executescript(schema)
#        conn.execute("""
#        insert into project (name, description, deadline)
#        values ('pymotw', 'Python Module of the Week', '2010-11-01')
#        """)



#def create_db_tbl(path2db, table=None, fields=None):
#    """Create the table 'table' with 'fields' in the database at path2db.
#
#    If table and fields are excluded, only the database will be created.
#
#    variables: path2db (string), table (string), fields (list)
#    returns None
#
#    TODO:  Should be able to take fields of different types, possibly as a
#           list of tuples.
#    """
#    with connect(path2db) as conn:
#        if table and fields:
#            c = conn.cursor()
#            # Builds the string of: key TEXT, ...for each field.
#            fields = ', '.join([' '.join([f, 'TEXT']) for f in fields])
#            sql_stmt = ' '.join(['CREATE TABLE IF NOT EXISTS', table, '(', fields, ')'])
#            c.execute(sql_stmt)
#            conn.commit()




#===============================================================================
# Changes
# * Using context manager in conn_and_exec rather than connect & close.
#===============================================================================
# Notes
# SQL wildcards: %val%val% for multiple args.
# Put values inside a tuple to prevent SQL-injection.
#===============================================================================

def connector(func, *args, **kwargs):
    def execute(*args, **kwargs):
        with connect('/home/na/whois.db') as conn:
            c = conn.cursor()

            stmt, vals = func(*args, **kwargs)
            c.execute(stmt, vals)

            conn.commit()

            # Will this return anything if I'm only inserting?
            return c.fetchall()

    return execute



@connector
def selectall_from(s, fld, part=False, tbl='botnet'):
    s = s if part is False else s.join(['%', '%'])
    stmt = f'SELECT * FROM {tbl} where {fld} like ?'
    return stmt, (s, )


@connector
def select_fields_from(fs, trgt, s, tbl='botnet', part=False):
    fs = ','.join(fs)
    s = s if part is False else s.join(['%', '%'])
    stmt = f'SELECT {fs} FROM {tbl} where {trgt}'
    stmt += '=?' if part is False else ' like ?'
    #print(stmt, (s, ))
    return stmt, (s, )



if __name__ == '__main__':
    results = select_fields_from(fs=('COUNTRY',),
                                 trgt='TIMESTAMP',
                                 s='2017-12-10',
                                 part=True)
    rsltlen = len(results)
    print(rsltlen) # 329
