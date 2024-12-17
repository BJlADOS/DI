# Задание 1
# 	Дан файл с некоторыми данными. Формат файла – произвольный. Считайте данные из файла и запишите их в Mongo. Реализуйте и выполните следующие запросы:
# 	вывод* первых 10 записей, отсортированных по убыванию по полю salary;
# 	вывод первых 15 записей, отфильтрованных по предикату age < 30, отсортировать по убыванию по полю salary
# 	вывод первых 10 записей, отфильтрованных по сложному предикату: (записи только из произвольного города, записи только из трех произвольно взятых профессий), отсортировать по возрастанию по полю age
# 	вывод количества записей, получаемых в результате следующей фильтрации (age в произвольном диапазоне, year в [2019,2022], 50 000 < salary <= 75 000 || 125 000 < salary < 150 000).
# * – здесь и везде предполагаем вывод в JSON.

import pymongo
import msgpack
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["mycollection"]

with open('./data/task_1_item.msgpack', 'rb') as file:
    data = msgpack.unpackb(file.read(), raw=False)

collection.insert_many(data)

def convert_objectid(data):
    if isinstance(data, list):
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
    return data

query1 = collection.find().sort("salary", pymongo.DESCENDING).limit(10)
with open('results/task1/query1.json', 'w', encoding='utf-8') as f:
    json.dump(convert_objectid(list(query1)), f, ensure_ascii=False, indent=4)

query2 = collection.find({"age": {"$lt": 30}}).sort("salary", pymongo.DESCENDING).limit(15)
with open('results/task1/query2.json', 'w', encoding='utf-8') as f:
    json.dump(convert_objectid(list(query2)), f, ensure_ascii=False, indent=4)

city = "Тбилиси"
jobs = ["Программист", "Инженер", "Менеджер"]
query3 = collection.find({"city": city, "job": {"$in": jobs}}).sort("age", pymongo.ASCENDING).limit(10)
with open('results/task1/query3.json', 'w', encoding='utf-8') as f:
    json.dump(convert_objectid(list(query3)), f, ensure_ascii=False, indent=4)

age_range = {"$gte": 25, "$lte": 35}
query4 = collection.count_documents({
    "age": age_range,
    "year": {"$in": [2019, 2022]},
    "$or": [
        {"salary": {"$gt": 50000, "$lte": 75000}},
        {"salary": {"$gt": 125000, "$lt": 150000}}
    ]
})
with open('results/task1/query4.json', 'w', encoding='utf-8') as f:
    json.dump({"count": query4}, f, ensure_ascii=False, indent=4)