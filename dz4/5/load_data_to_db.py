import sqlite3
import csv

conn = sqlite3.connect('bookstore.db')
cursor = conn.cursor()

def load_csv(file_path, table_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Пропуск заголовков
        placeholders = ','.join(['?'] * len(next(reader)))
        f.seek(0)
        next(reader)
        cursor.executemany(f'INSERT INTO {table_name} VALUES ({placeholders})', reader)

load_csv('authors.csv', 'Authors')
load_csv('books.csv', 'Books')
load_csv('sales.csv', 'Sales')

conn.commit()
conn.close()
