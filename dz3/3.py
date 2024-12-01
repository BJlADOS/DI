# Задание 3
# Исследовать структуру xml-файлов, чтобы произвести парсинг всех данных. В каждом файле содержится информация об одном объекте из случайной предметной области. Полученные данные собрать и записать в json. Выполните также ряд операций с данными:
# 	отсортируйте значения по одному из доступных полей
# 	выполните фильтрацию по другому полю (запишите результат отдельно)
# 	для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
# 	для одного текстового поля посчитайте частоту меток

import os
import json
import xml.etree.ElementTree as ET
import pandas as pd

xml_dir = './data/3'

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    star_data = {
        'name': root.find('name').text.strip(),
        'constellation': root.find('constellation').text.strip(),
        'spectral_class': root.find('spectral-class').text.strip(),
        'radius': int(root.find('radius').text),
        'rotation_days': float(root.find('rotation').text.split()[0]),
        'age_billion_years': float(root.find('age').text.split()[0]),
        'distance_million_km': float(root.find('distance').text.split()[0]),
        'absolute_magnitude_million_km': float(root.find('absolute-magnitude').text.split()[0])
    }
    return star_data

stars = []
for file_name in os.listdir(xml_dir):
    if file_name.endswith('.xml'):
        file_path = os.path.join(xml_dir, file_name)
        star_data = parse_xml(file_path)
        stars.append(star_data)

with open('./data/third_task_stars.json', 'w', encoding='utf-8') as json_file:
    json.dump(stars, json_file, ensure_ascii=False, indent=4)

df = pd.DataFrame(stars)

sorted_stars = df.sort_values('age_billion_years')
sorted_stars.to_json('./data/third_task_sorted_stars.json', orient='records', force_ascii=False, indent=4)

filtered_stars = df[df['constellation'] == 'Лев'].to_json('./data/third_task_filtered_stars.json', orient='records', force_ascii=False, indent=4)

radius_stats = {
    'sum': float(df['radius'].sum()),
    'min': float(df['radius'].min()),
    'max': float(df['radius'].max()),
    'mean': float(df['radius'].mean())
}

constellation_frequency = df['constellation'].value_counts().to_json('./data/third_task_constellation_frequency.json', force_ascii=False, indent=4)

with open('./data/third_task_radius_stats.json', 'w', encoding='utf-8') as json_file:
    json.dump(radius_stats, json_file, ensure_ascii=False, indent=4)
