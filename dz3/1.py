# Задание 1
# Исследовать структуру html-файлов, чтобы произвести парсинг всех данных. В каждом файле содержится информация об одном объекте из случайной предметной области. Полученные данные собрать и записать в json. Выполните также ряд операций с данными:
# 	отсортируйте значения по одному из доступных полей
# 	выполните фильтрацию по другому полю (запишите результат отдельно)
# 	для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
# 	для одного текстового поля посчитайте частоту меток

import json
import os
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime

data = []
for filename in os.listdir('./data/1'):
    with open(f'./data/1/{filename}', 'r', encoding='utf-8') as file:
        item = {}
        soup = BeautifulSoup(file, 'html.parser')
        chess_tournament = soup.find('div', class_='chess-wrapper')
        item['type'] = chess_tournament.find('span').text.strip().split(': ')[1].strip()
        item['id'] = chess_tournament.find('h1', class_='title').get('id')
        item['tournament'] = chess_tournament.find('h1', class_='title').text.strip().split(':')[1].strip()
        adress_p = [w.strip() for w in chess_tournament.find('p', class_='address-p').text.strip().split(':')]
        if len(adress_p) == 3:
            for i in range(1 ,len(adress_p[1])):
                if (adress_p[1][i].isupper() and adress_p[1][i:]=='Начало') or adress_p[1][i] == '\n':
                    adress_p[1] = adress_p[1][:i]
                    break
        item['city'] = adress_p[1].strip()
        #get year with regex
        year = re.findall(r'\d{4}', chess_tournament.find('h1', class_='title').text.strip().split(':')[1].strip())
        item['start'] = f'{adress_p[2]}.{year[0]}'
        print(adress_p)
        item['tours'] = int(chess_tournament.find('span', class_='count').text.strip().split(':')[1].strip())
        item['time_control'] = chess_tournament.find('span', class_='year').text.strip().split(':')[1].strip()
        item['min_rating'] = int(chess_tournament.find_all('span')[3].text.strip().split(':')[1].strip())
        item['img'] = chess_tournament.find('img').get('src')
        item['rating'] = float(chess_tournament.find_all('span')[4].text.strip().split(':')[1].strip())
        item['views'] = int(chess_tournament.find_all('span')[5].text.strip().split(':')[1].strip())
        data.append(item)

with open('./data/first_task_result.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

for item in data:
    item['start'] = datetime.strptime(item['start'], '%d.%m.%Y')
data = sorted(data, key=lambda x: x['start'])
for item in data:
    item['start'] = item['start'].strftime('%d.%m.%Y')
with open('./data/first_task_result.json_sorted.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

views = [item for item in data if item['views'] > 50000]
with open('./data/first_task_result.json_filtered.json', 'w', encoding='utf-8') as file:
    json.dump(views, file, indent=4, ensure_ascii=False)

df = pd.DataFrame(data)
rating_stats = df['rating'].describe()
print(rating_stats)

type_freq = df['type'].value_counts()
print(type_freq)
