import sqlite3

conn = sqlite3.connect('bookstore.db')
cursor = conn.cursor()

with open('init_db.sql', 'r', encoding='utf-8') as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()
