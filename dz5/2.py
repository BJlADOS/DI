# Дан файл с некоторыми данными. Формат файла – произвольный, не совпадает с тем, что был в первом задании. Необходимо считать данные и добавить их к той коллекции, куда были записаны данные в первом задании. Реализовать следующие запросы:
# 	вывод минимальной, средней, максимальной salary
# 	вывод количества данных по представленным профессиям
# 	вывод минимальной, средней, максимальной salary по городу
# 	вывод минимальной, средней, максимальной salary по профессии
# 	вывод минимального, среднего, максимального возраста по городу
# 	вывод минимального, среднего, максимального возраста по профессии
# 	вывод максимальной заработной платы при минимальном возрасте
# 	вывод минимальной заработной платы при максимальной возрасте
# 	вывод минимального, среднего, максимального возраста по городу, при условии, что заработная плата больше 50 000, отсортировать вывод по убыванию по полю avg
# 	вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах по городу, профессии, и возрасту: 18<age<25 & 50<age<65
# 	произвольный запрос с $match, $group, $sort

import pymongo
import pickle as pkl
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["mycollection"]

with open('./data/task_2_item.pkl', 'rb') as file:
    new_data = pkl.load(file)

collection.insert_many(new_data)

def save_to_json(filename, data):
    with open(f'./results/task2/{filename}', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

pipeline_salary = [
    {"$group": {
        "_id": None,
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]
result_salary = list(collection.aggregate(pipeline_salary))
save_to_json('result_salary.json', result_salary)

pipeline_professions = [
    {"$group": {
        "_id": "$job",
        "count": {"$sum": 1}
    }}
]
result_professions = list(collection.aggregate(pipeline_professions))
save_to_json('result_professions.json', result_professions)

pipeline_salary_city = [
    {"$group": {
        "_id": "$city",
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]
result_salary_city = list(collection.aggregate(pipeline_salary_city))
save_to_json('result_salary_city.json', result_salary_city)

pipeline_salary_job = [
    {"$group": {
        "_id": "$job",
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]
result_salary_job = list(collection.aggregate(pipeline_salary_job))
save_to_json('result_salary_job.json', result_salary_job)

pipeline_age_city = [
    {"$group": {
        "_id": "$city",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }}
]
result_age_city = list(collection.aggregate(pipeline_age_city))
save_to_json('result_age_city.json', result_age_city)

pipeline_age_job = [
    {"$group": {
        "_id": "$job",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }}
]
result_age_job = list(collection.aggregate(pipeline_age_job))
save_to_json('result_age_job.json', result_age_job)

pipeline_max_salary_min_age = [
    {"$sort": {"age": 1, "salary": -1}},
    {"$limit": 1},
    {"$project": {"_id": 0, "age": 1, "salary": 1}}
]
result_max_salary_min_age = list(collection.aggregate(pipeline_max_salary_min_age))
save_to_json('result_max_salary_min_age.json', result_max_salary_min_age)

pipeline_min_salary_max_age = [
    {"$sort": {"age": -1, "salary": 1}},
    {"$limit": 1},
    {"$project": {"_id": 0, "age": 1, "salary": 1}}
]
result_min_salary_max_age = list(collection.aggregate(pipeline_min_salary_max_age))
save_to_json('result_min_salary_max_age.json', result_min_salary_max_age)

pipeline_age_city_salary = [
    {"$match": {"salary": {"$gt": 50000}}},
    {"$group": {
        "_id": "$city",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }},
    {"$sort": {"avg_age": -1}}
]
result_age_city_salary = list(collection.aggregate(pipeline_age_city_salary))
save_to_json('result_age_city_salary.json', result_age_city_salary)

pipeline_salary_ranges = [
    {"$match": {"$or": [{"age": {"$gt": 18, "$lt": 25}}, {"age": {"$gt": 50, "$lt": 65}}]}},
    {"$group": {
        "_id": {"city": "$city", "job": "$job"},
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]
result_salary_ranges = list(collection.aggregate(pipeline_salary_ranges))
save_to_json('result_salary_ranges.json', result_salary_ranges)

pipeline_custom = [
    {"$match": {"city": "Москва"}},
    {"$group": {
        "_id": "$job",
        "total_salary": {"$sum": "$salary"}
    }},
    {"$sort": {"total_salary": -1}}
]
result_custom = list(collection.aggregate(pipeline_custom))
save_to_json('result_custom.json', result_custom)
