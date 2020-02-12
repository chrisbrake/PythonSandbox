import sqlite3

connection = sqlite3.connect('example.db')
cursor = connection.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks
    (date text, trans text, symbol text, qty real, price real)
    ''')

# Insert a row of data
cursor.execute("""
    INSERT INTO stocks 
    VALUES ('2006-01-05','BUY','RHAT',100,35.14)
    """)

# Save (commit) the changes
connection.commit()

# Do this style value substitution
t = ('RHAT',)
cursor.execute('''
    SELECT * 
    FROM stocks 
    WHERE symbol=?
    ''', t)
print(cursor.fetchone())

# Larger example that inserts many records at a time
cursor.executemany('''
    INSERT INTO stocks 
    VALUES (?,?,?,?,?)
    ''', [
    ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
    ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
    ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
    ]
)

for row in cursor.execute('SELECT * FROM stocks ORDER BY price'):
    print(row)
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
connection.close()

# See also: https://docs.python.org/3.8/library/sqlite3.html#sqlite3.Connection.create_function
