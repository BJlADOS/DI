# Самостоятельно найти сайт, соответствующий следующим условиям:
# 	непопулярный, регионального уровня или из узкой области (с целью избежать дублирования)
# 	наличие страниц-каталогов, где есть информация сразу по нескольких объектам
# 	наличие страниц, посвященных отдельному объекту
#  Необходимо:
# 	спарсить нескольких страниц (минимум 10), посвященных только одному объекту;
# 	спарсить страницы-каталоги, где размещена информация сразу по нескольким объектам.
# Данные можно скачать и сохранить локально в виде html, а можно организовать их получение напрямую через обращение к серверу сайта.
# Результаты парсинга собрать отдельно по каждой подзадаче и записать в отдельный json.
# Выполните произвольные операции с данными:
# 	отсортируйте значения по одному из доступных полей
# 	выполните фильтрацию по другому полю (запишите результат отдельно)
# 	для одного выбранного числового поля посчитайте показатели статистики
# 	для одного текстового поля посчитайте частоту меток.
import re

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

prefix = 'https://elema.ru'

def get_html(url):
    response = requests.get(url)
    return response.text

def extract_product_paths(catalog_url):
    html = get_html(catalog_url)
    soup = BeautifulSoup(html, 'html.parser')
    product_paths = []
    for link in soup.find_all('a', { 'class': 'g-pos-abs g-height-100x g-width-100x g-z-index-2' }):
        product_paths.append(prefix + link['href'])
    return product_paths

def parse_catalog_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    for item in soup.select('.product_image'):
        title = item.select_one('.g-color-bluegray--hover').text.strip()
        price = item.select_one('.g-font-weight-600').text.strip()
        old_price = item.select_one('span[style*="line-through"]').text.strip()
        items.append({
            'title': title,
            'price': int(price.replace(' руб', '').replace(' ', '')),
            'old_price': int(old_price.replace(' руб', '').replace(' ', ''))
        })
    return items

def parse_object_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('h1').text.strip()
    price = soup.find('span', { 'class': 'newprice' }).text.strip()
    old_price = soup.find('span', { 'class': 'product-item-detail-price-old' }).text.strip()
    print(title)
    season_regex = re.findall(re.compile(r'Сезон:[\n ](.*)\n'), soup.find('div', { 'class': 'u-accordion__body g-pa-15-0' }).text.strip())
    if len(season_regex) == 0:
        season = 'Не указано'
    else:
        season = season_regex[0].strip()
    print(season.replace('\t', ''))
    place_of_origin = soup.find('div', { 'class': 'u-accordion__body g-pa-15-0' }).find_all('div')[2].text.strip().split(':')[1].strip()
    return {
        'title': title,
        'price': int(price.replace(' руб', '').replace(' ', '')),
        'old_price': int(old_price),
        'season': season.replace('\t', ''),
        'place_of_origin': place_of_origin
    }

catalog_urls = [
    'https://elema.ru/catalog/zhenskaya-odezhda/bluzki/?PAGEN_1=1',
    'https://elema.ru/catalog/zhenskaya-odezhda/bluzki/?PAGEN_1=2',
    'https://elema.ru/catalog/zhenskaya-odezhda/bluzki/?PAGEN_1=3',
    'https://elema.ru/catalog/zhenskaya-odezhda/bluzki/?PAGEN_1=4',
    'https://elema.ru/catalog/zhenskaya-odezhda/bluzki/?PAGEN_1=5',
    'https://elema.ru/catalog/zhenskaya-odezhda/bluzki/?PAGEN_1=6',
    'https://elema.ru/catalog/zhenskaya-odezhda/bluzki/?PAGEN_1=7',
    'https://elema.ru/catalog/zhenskaya-odezhda/bluzki/?PAGEN_1=8',
    'https://elema.ru/catalog/zhenskaya-odezhda/bluzki/?PAGEN_1=9',
    'https://elema.ru/catalog/zhenskaya-odezhda/bluzki/?PAGEN_1=10',
]

all_product_paths = []
for url in catalog_urls:
    all_product_paths.extend(extract_product_paths(url))

catalog_data = []
for url in catalog_urls:
    catalog_data.extend(parse_catalog_page(url))

object_data = []
for url in all_product_paths:
    object_data.append(parse_object_page(url))

with open('./data/fifth_task_catalog_data.json', 'w', encoding='utf-8') as f:
    json.dump(catalog_data, f, ensure_ascii=False, indent=4)

with open('./data/fifth_task_object_data.json', 'w', encoding='utf-8') as f:
    json.dump(object_data, f, ensure_ascii=False, indent=4)

df = pd.DataFrame(object_data)
sorted_data = df.sort_values(by='price')
sorted_data.to_json('./data/fifth_task_sorted_data.json', orient='records', force_ascii=False, indent=4)

filtered_data = df[df['old_price'] - df['price'] > 1000]
filtered_data.to_json('./data/fifth_task_filtered_data.json', orient='records', force_ascii=False, indent=4)

price_stats = {
    'mean': float(df['price'].mean()),
    'std': float(df['price'].std()),
    'min': float(df['price'].min()),
    'max': float(df['price'].max())
}

title_counts = df['season'].value_counts().to_dict()

with open('./data/fifth_task_price_stats.json', 'w', encoding='utf-8') as f:
    json.dump(price_stats, f, ensure_ascii=False, indent=4)

with open('./data/fifth_task_title_counts.json', 'w', encoding='utf-8') as f:
    json.dump(title_counts, f, ensure_ascii=False, indent=4)
