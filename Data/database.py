import sqlite3

conn = sqlite3.connect('high_scores.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE customers (
        username text,
        password text,
        
    )""")

cursor.execute("INSERT INTO customers VALUES ('John', 'Elder', 'john@codemy.com')")

conn.commit()
conn.close()
