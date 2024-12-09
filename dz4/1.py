# Задание 1
# 	Дан файл с некоторыми данными. Формат файла – произвольный. Спроектируйте на его основе и создайте таблицу в базе данных (SQLite). Считайте данные из файла и запишите их в созданную таблицу. Реализуйте и выполните следующие запросы:
# 	вывод первых (VAR+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json;
# 	вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
# 	вывод частоты встречаемости для категориального поля;
# 	вывод первых (VAR+10) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.

import sqlite3
import msgpack
import json

with open('./data/1-2/item.msgpack', 'rb') as f:
    data = msgpack.unpack(f, raw=False)

print(data)
conn = sqlite3.connect('first_task_books.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        isbn TEXT PRIMARY KEY,
        rating REAL,
        views INTEGER,
        title TEXT,
        author TEXT,
        genre TEXT,
        pages INTEGER,
        published_year INTEGER
    )
''')

for item in data:
    cursor.execute('''
        INSERT INTO books (isbn, rating, views, title, author, genre, pages, published_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (item['isbn'], item['rating'], item['views'], item['title'], item['author'], item['genre'], item['pages'], item['published_year']))

conn.commit()

cursor.execute('SELECT * FROM books ORDER BY rating LIMIT 11')
rows = cursor.fetchall()
with open('first_task_sorted_books.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=4)

cursor.execute('SELECT SUM(views), MIN(views), MAX(views), AVG(views) FROM books')
stats = cursor.fetchone()
print(f'Сумма: {stats[0]}, Мин: {stats[1]}, Макс: {stats[2]}, Среднее: {stats[3]}')

cursor.execute('SELECT genre, COUNT(*) FROM books GROUP BY genre')
genre_counts = cursor.fetchall()
for genre, count in genre_counts:
    print(f'Жанр: {genre}, Количество: {count}')

cursor.execute('SELECT * FROM books WHERE views > 100 ORDER BY rating LIMIT 11')
filtered_rows = cursor.fetchall()
with open('first_task_filtered_sorted_books.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_rows, f, ensure_ascii=False, indent=4)

conn.close()