# Дано два файла разных форматов. Необходимо проанализировать их структуру и выделить общие хранимые данные. Необходимо создать таблицу для хранения данных в базе данных. Произведите запись данных из файлов разных форматов в одну таблицу. Реализуйте и выполните следующие запросы:
# 	вывод первых (1+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json;
# 	вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
# 	вывод частоты встречаемости для категориального поля;
# 	вывод первых (1+15) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.

import pandas as pd
import sqlite3
import msgpack

with open('./data/3/_part_1.msgpack', 'rb') as f:
    data_part1 = pd.DataFrame(msgpack.unpack(f, raw=False))
data_part2 = pd.DataFrame(pd.read_pickle('./data/3/_part_2.pkl'))

conn = sqlite3.connect('third_task_music_data.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS music (
    artist TEXT,
    song TEXT,
    duration_ms INTEGER,
    year INTEGER,
    tempo REAL,
    genre TEXT,
    mode INTEGER,
    speechiness REAL,
    acousticness REAL,
    instrumentalness REAL,
    energy REAL,
    popularity INTEGER
)
''')

data_part1.to_sql('music', conn, if_exists='append', index=False)
data_part2.to_sql('music', conn, if_exists='append', index=False)

query = 'SELECT * FROM music ORDER BY duration_ms LIMIT 11'
result = pd.read_sql(query, conn)
result.to_json('third_task_sorted_duration.json', orient='records', lines=True)

query = 'SELECT SUM(duration_ms), MIN(duration_ms), MAX(duration_ms), AVG(duration_ms) FROM music'
result = pd.read_sql(query, conn)
print(result)

query = 'SELECT genre, COUNT(*) as frequency FROM music GROUP BY genre'
result = pd.read_sql(query, conn)
print(result)

query = 'SELECT * FROM music WHERE year > 2010 ORDER BY popularity LIMIT 16'
result = pd.read_sql(query, conn)
result.to_json('third_task_filtered_sorted_popularity.json', orient='records', lines=True)

conn.close()