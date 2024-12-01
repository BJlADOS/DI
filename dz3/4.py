# Задание 4
# Исследовать структуру xml-файлов, чтобы произвести парсинг всех данных. В каждом файле содержится информация об одном или нескольких объектах из случайной предметной области. Перечень всех характеристик объекта может меняться (у отдельного объекта могут отсутствовать некоторые характеристики). Полученные данные собрать и записать в json. Выполните также ряд операций с данными:
# 	отсортируйте значения по одному из доступных полей
# 	выполните фильтрацию по другому полю (запишите результат отдельно)
# 	для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
# 	для одного текстового поля посчитайте частоту меток

import os
import json
import xml.etree.ElementTree as ET
import pandas as pd

xml_dir = './data/4'

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    clothing_items = []
    for clothing in root.findall('clothing'):
        item = {}
        for child in clothing:
            item[child.tag] = child.text.strip() if child.text else None
        clothing_items.append(item)
    return clothing_items

all_clothing_items = []
for file_name in os.listdir(xml_dir):
    if file_name.endswith('.xml'):
        file_path = os.path.join(xml_dir, file_name)
        clothing_items = parse_xml(file_path)
        all_clothing_items.extend(clothing_items)

with open('./data/fourth_task_clothing_items.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_clothing_items, json_file, ensure_ascii=False, indent=4)

df = pd.DataFrame(all_clothing_items)

df['price'] = pd.to_numeric(df['price'], errors='coerce')
sorted_clothing_items = df.sort_values('price')
sorted_clothing_items.to_json('./data/fourth_task_sorted_clothing_items.json', orient='records', force_ascii=False, indent=4)

filtered_clothing_items = df[df['category'] == 'T-shirt']
filtered_clothing_items.to_json('./data/fourth_task_filtered_clothing_items.json', orient='records', force_ascii=False, indent=4)

df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
rating_stats = {
    'sum': float(df['rating'].sum()),
    'min': float(df['rating'].min()),
    'max': float(df['rating'].max()),
    'mean': float(df['rating'].mean())
}

color_frequency = df['color'].value_counts().to_dict()

with open('./data/fourth_task_rating_stats.json', 'w', encoding='utf-8') as json_file:
    json.dump(rating_stats, json_file, ensure_ascii=False, indent=4)

with open('./data/fourth_task_color_frequency.json', 'w', encoding='utf-8') as json_file:
    json.dump(color_frequency, json_file, ensure_ascii=False, indent=4)