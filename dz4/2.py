# Задание 2
# Дан файл с некоторыми данными. Формат файла – произвольный. Данные некоторым образом связаны с теми, что были добавлены в первом задании. Необходимо проанализировать и установить связь между таблицами. Создать таблицу и наполнить ее прочитанными данными из файла. Реализовать и выполнить 3 запроса, где используется связь между таблицами.

import sqlite3

with open('./data/1-2/subitem.text', 'r', encoding='utf-8') as f:
    lines = f.read().split('=====')

data = []
for line in lines:
    if line.strip():
        item = {}
        for field in line.strip().split('\n'):
            key, value = field.split('::')
            item[key.strip()] = value.strip()
        data.append(item)

conn = sqlite3.connect('first_task_books.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS subitems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT REFERENCES books(title),
        price INTEGER,
        place TEXT,
        date TEXT
    )
''')

for item in data:
    cursor.execute('''
        INSERT INTO subitems (title, price, place, date)
        VALUES (?, ?, ?, ?)
    ''', (item['title'], item['price'], item['place'], item['date']))

conn.commit()

cursor.execute('''
    SELECT b.title, b.author, s.price, s.place
    FROM books b
    JOIN subitems s ON b.title = s.title
''')
result1 = cursor.fetchall()
print(result1)

cursor.execute('''
    SELECT s.place, COUNT(*), AVG(s.price)
    FROM subitems s
    JOIN books b ON b.title = s.title
    GROUP BY s.place
''')
result2 = cursor.fetchall()
print(result2)

cursor.execute('''
    SELECT b.title, s.price, s.date
    FROM books b
    JOIN subitems s ON b.title = s.title
    WHERE s.price > 2000
    ORDER BY s.date DESC
''')
result3 = cursor.fetchall()
print(result3)

conn.close()