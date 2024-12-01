# Задание 2
# Исследовать структуру html-файлов, чтобы произвести парсинг всех данных. В каждом файле содержится информация об одном или нескольких объектах из случайной предметной области. Перечень всех характеристик объекта может меняться (у отдельного объекта могут отсутствовать некоторые характеристики). Полученные данные собрать и записать в json. Выполните также ряд операций с данными:
# 	отсортируйте значения по одному из доступных полей
# 	выполните фильтрацию по другому полю (запишите результат отдельно)
# 	для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
# 	для одного текстового поля посчитайте частоту меток

import json
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

def df_to_formatted_json(df, sep="."):
    """
    The opposite of json_normalize
    """
    result = []
    for idx, row in df.iterrows():
        parsed_row = {}
        for col_label,v in row.items():
            keys = col_label.split(sep)

            current = parsed_row
            for i, k in enumerate(keys):
                if i==len(keys)-1:
                    if not pd.isna(v):
                        current[k] = v
                else:
                    if k not in current.keys():
                        current[k] = {}
                    current = current[k]
        # save
        result.append(parsed_row)
    return result

products = []
for filename in os.listdir('./data/2'):
    with open(f'./data/2/{filename}', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    for product in soup.find_all('div', class_='product-item'):
        data = {
            'id': product.find('a', class_='add-to-favorite')['data-id'],
            'name': product.find('span').text.strip(),
            'price': int(product.find('price').text.strip().replace('₽', '').replace(' ', '')),
            'bonus': int(re.findall(re.compile(r'\d+'), product.find('strong').text.strip())[0]),
            'characteristics': {}
        }
        for li in product.find_all('li'):
            data['characteristics'][li['type']] = li.text.strip()
        products.append(data)

with open('./data/second_task_products.json', 'w', encoding='utf-8') as json_file:
    json.dump(products, json_file, ensure_ascii=False, indent=4)

df = pd.json_normalize(products, sep='_', max_level=1)
print(df)

sorted_df = df.sort_values(by='price')
with open('./data/second_task_sorted_products.json', 'w', encoding='utf-8') as json_file:
    json.dump(df_to_formatted_json(sorted_df, '_'), json_file, ensure_ascii=False, indent=4)

filtered_df = df[df['characteristics_sim'] == '2 SIM']
with open('./data/second_task_filtered_products.json', 'w', encoding='utf-8') as json_file:
    json.dump(df_to_formatted_json(filtered_df, '_'), json_file, ensure_ascii=False, indent=4)

price_stats = {
    'sum': float(df['price'].sum()),
    'min': float(df['price'].min()),
    'max': float(df['price'].max()),
    'mean': float(df['price'].mean())
}
with open('./data/second_task_price_stats.json', 'w', encoding='utf-8') as json_file:
    json.dump(price_stats, json_file, ensure_ascii=False, indent=4)

name_frequency = df['name'].value_counts().to_dict()
with open('./data/second_task_name_frequency.json', 'w', encoding='utf-8') as json_file:
    json.dump(name_frequency, json_file, ensure_ascii=False, indent=4)
