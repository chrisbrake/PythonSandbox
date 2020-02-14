import os
import sqlite3
import textwrap

DB_PATH = os.environ.get('DB_PATH') or 'example.db'

# connection = sqlite3.connect(DB_PATH)
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks
    (date text, trans text, symbol text, qty real, price real)
    ''')

# Save (commit) the changes
connection.commit()

# print('We can easily insert many records at a time')
cursor.executemany(
    '''
    INSERT INTO stocks 
    VALUES (?,?,?,?,?)
    ''', [
        ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
        ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
        ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
        ('2006-01-05', 'BUY', 'RHAT', 100, 35.14),
    ]
)

print('You can iterate over the result in batches using cursor.fetchmany')
cursor.execute('SELECT * FROM stocks ORDER BY price')
batch = None
i = 1
while batch or batch is None:
    batch = cursor.fetchmany(3)
    print(f'\tBatch {i}: {batch}')
    i = i + 1

# Create a key-value data store
cursor.execute('''
    CREATE TABLE IF NOT EXISTS kvs (key, value)
    ''')

cursor.executemany(
    '''
    INSERT INTO kvs 
    VALUES (?,?)
    ''', [
        ("2006-03-28", 45.00),
        ('2006-04-05', 'BUY'),
        ('2006-04-06', 500),
    ]
)

# Save (commit) the changes again
connection.commit()
values = [row for row in cursor.execute("SELECT * FROM kvs")]
print(textwrap.dedent(f'''
    We can build a key/value store with mixed values: {values}
'''))

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
connection.close()

print('We can store store functions in the connection to the database.')


def sqlite_function(s):
    """
    A method that will be passed into sqlite to be run as part of a query

    :param s: argument
    :return: a string
    """
    return f'sqlite_function({s})'


con = sqlite3.connect('example.db')
con.create_function('function', 1, sqlite_function)
cur = con.cursor()
cur.execute('select function(?)', ('argument',))
print(f'They can be executed as part of a select statement: {cur.fetchmany()}')
con.close()
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

try:
    cur.execute(
        '''
        select function('foo')
        ''',
    )
except sqlite3.OperationalError as e:
    print(textwrap.dedent(f'''
        But, they are a property of the connection and need to be explicitly 
        included every time you reconnect connection the function is lost.
        Otherwise you will see a "{e}" error.
    '''))
con.close()
