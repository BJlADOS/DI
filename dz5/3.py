# Задание 3
# Дан файл с некоторыми данными. Формат файла – произвольный, не совпадает с тем, что был в первом/втором заданиях. Необходимо считать данные и добавить их к той коллекции, куда были записаны данные в первом и втором заданиях. Выполните следующие запросы:
# 	удалить из коллекции документы по предикату: salary < 25 000 || salary > 175000
# 	увеличить возраст (age) всех документов на 1
# 	поднять заработную плату на 5% для произвольно выбранных профессий
# 	поднять заработную плату на 7% для произвольно выбранных городов
# 	поднять заработную плату на 10% для выборки по сложному предикату (произвольный город, произвольный набор профессий, произвольный диапазон возраста)
# 	удалить из коллекции записи по произвольному предикату

import pandas as pd
from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('localhost', 27017)
db = client['mydb']
collection = db['mycollection']

# Чтение данных из CSV файла
data = pd.read_csv('./data/task_3_item.csv')

# Преобразование данных в список словарей
data_dict = data.to_dict('records')

# Добавление данных в коллекцию
collection.insert_many(data_dict)

# Удаление документов по предикату: salary < 25 000 || salary > 175000
collection.delete_many({'$or': [{'salary': {'$lt': 25000}}, {'salary': {'$gt': 175000}}]})

# Увеличение возраста (age) всех документов на 1
collection.update_many({}, {'$inc': {'age': 1}})

# Поднятие заработной платы на 5% для произвольно выбранных профессий
professions = ['Инженер', 'Учитель']  # Пример произвольных профессий
collection.update_many({'profession': {'$in': professions}}, {'$mul': {'salary': 1.05}})

# Поднятие заработной платы на 7% для произвольно выбранных городов
cities = ['Москва', 'Санкт-Петербург']  # Пример произвольных городов
collection.update_many({'city': {'$in': cities}}, {'$mul': {'salary': 1.07}})

# Поднятие заработной платы на 10% для выборки по сложному предикату
complex_predicate = {
    'city': 'Тбилиси',
    'profession': {'$in': ['Врач', 'Архитектор']},
    'age': {'$gte': 30, '$lte': 40}
}
collection.update_many(complex_predicate, {'$mul': {'salary': 1.10}})

# Удаление из коллекции записи по произвольному предикату
random_predicate = {'city': 'Сан-Франциско'}  # Пример произвольного предиката
collection.delete_many(random_predicate)