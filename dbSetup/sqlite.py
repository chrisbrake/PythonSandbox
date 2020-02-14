import sqlite3
import textwrap

connection = sqlite3.connect("example.db")
# connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks
    (date text, trans text, symbol text, qty real, price real)
    ''')

# Insert a row of data
cursor.execute(
    """
    INSERT INTO stocks 
    VALUES ('2006-01-05','BUY','RHAT',100,35.14)
    """
)

# Save (commit) the changes
connection.commit()

# Do this style value substitution
t = ('RHAT',)
cursor.execute(
    '''
    SELECT * 
    FROM stocks 
    WHERE symbol=?
    ''', t
)
print(cursor.fetchone())

# Larger example that inserts many records at a time
cursor.executemany(
    '''
    INSERT INTO stocks 
    VALUES (?,?,?,?,?)
    ''', [
        ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
        ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
        ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
    ]
)

print('You can iterate over the result in batches using cursor.fetchmany')
cursor.execute('SELECT * FROM stocks ORDER BY price')
for batch in cursor.fetchmany(2):
    print(f'{[i for i in batch]}')

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
print('And now we have a key/value store.')
print([row for row in cursor.execute('SELECT * FROM kvs')])


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
connection.close()

print('We can create functions and store them in the database.')


def sqlite_function(s):
    return s


con = sqlite3.connect('example.db')
con.create_function('function', 1, sqlite_function)
cur = con.cursor()
cur.execute('select function(?)', (b"foo",))
print(f'They can be executed as part of a select statement: {cur.fetchmany()}')

cur.execute(
    '''
    select function('foo')
    ''',
)
print(cur.fetchmany())

cur.execute(
    '''
    select function('foo')
    ''',
)
print(cur.fetchmany())


con.close()
con = sqlite3.connect('example.db')
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
