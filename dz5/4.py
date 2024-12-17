# Задание 4
# Самостоятельно выбрать предметную область. Подобрать пару наборов данных разных форматов. Заполнение данных в mongo осуществляем из файлов. Реализовать выполнение по 5 запросов в каждой категорий:
# 	выборка (задание 1),
# 	выбора с агрегацией (задание 2)
# 	обновление/удаление данных (задание 3).

import pandas as pd
import msgpack
import pickle
import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["cosmetics_db"]
collection = db["products"]

collection.delete_many({})

csv_data = pd.read_csv('./data/cosmetics_set1.csv')

with open('./data/cosmetics_set2.msgpack', 'rb') as f:
    msgpack_data = msgpack.unpackb(f.read(), raw=False)

with open('./data/cosmetics_set3.pkl', 'rb') as f:
    pickle_data = pickle.load(f)

def convert_objectid(data):
    if isinstance(data, list):
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
    return data

msgpack_data = pd.DataFrame(msgpack_data)
pickle_data = pd.DataFrame(pickle_data)

collection.insert_many(csv_data.to_dict(orient='records'))
collection.insert_many(msgpack_data.to_dict(orient='records'))
collection.insert_many(pickle_data.to_dict(orient='records'))

def save_to_json(filename, data):
    with open(f'./results/task4/{filename}', 'w', encoding='utf-8') as f:
        json.dump(convert_objectid(data), f, ensure_ascii=False, indent=4)

result = list(collection.find().sort("price", -1).limit(10))
save_to_json('top_10_by_price.json', result)

result = list(collection.find({"rating": {"$gt": 4.5}}).sort("price", -1).limit(15))
save_to_json('top_15_by_rating_and_price.json', result)

result = list(collection.find({
    "category": "Lipstick",
    "brand": {"$in": ["Dior", "MAC", "Chanel"]}
}).sort("rating", 1).limit(10))
save_to_json('top_10_lipstick_by_rating.json', result)

count = collection.count_documents({
    "price": {"$gte": 20, "$lte": 50},
    "rating": {"$gte": 4.0}
})
save_to_json('count_price_20_50_rating_4.json', {"count": count})

result = list(collection.aggregate([
    {"$group": {
        "_id": None,
        "min_price": {"$min": "$price"},
        "avg_price": {"$avg": "$price"},
        "max_price": {"$max": "$price"}
    }}
]))
save_to_json('min_avg_max_price.json', result)

result = list(collection.aggregate([
    {"$group": {
        "_id": "$brand",
        "count": {"$sum": 1}
    }}
]))
save_to_json('count_by_brand.json', result)

collection.delete_many({"$or": [{"price": {"$lt": 15}}, {"price": {"$gt": 120}}]})

collection.update_many({}, {"$inc": {"rating": 0.1}})

collection.update_many({"category": "Foundation"}, {"$mul": {"price": 1.05}})

collection.delete_many({"reviews": 0})
