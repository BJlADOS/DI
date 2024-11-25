# Задание 5
# Найдите набор данных (csv, json), размер которого превышает 20-30Мб.
# Отберите для дальнейшей работы в нем 7-10 полей (пропишите это преобразование в коде). Для полей, представляющих числовые данные, рассчитайте характеристики: максимальное и минимальное значения, среднее арифметическое, сумму, стандартное отклонение. Для полей, представляющий текстовые данные (в виде меток некоторых категорий) рассчитайте частоту встречаемости. Сохраните полученные расчеты в json. Сохраните набор данных с помощью разных форматов: csv, json, msgpack, pkl. Сравните размеры полученных файлов.

import pandas as pd
import numpy as np
import json
import msgpack
import pickle
import os
# https://www.datablist.com/learn/csv/download-sample-csv-files Organizations CSV with 2000000 records
data = pd.read_csv('./data/organizations-2000000.csv', index_col='Index')

data = data[['Name', 'Website', 'Country', 'Description', 'Founded', 'Industry', 'Number of employees']]
data.columns = ['name', 'website', 'country', 'description', 'founded', 'industry', 'number_of_employees']

result = {}
for col in data.select_dtypes(include=np.number).columns:
    result[col] = {
        'max': float(data[col].max()),
        'min': float(data[col].min()),
        'mean': float(data[col].mean()),
        'sum': float(data[col].sum()),
        'std': float(data[col].std())
    }

for col in data.select_dtypes(include=np.object_).columns:
    result[col] = data[col].value_counts().to_dict()

with open('./data/fifth_task_result.json', 'w') as f:
    json.dump(result, f)

data.to_csv('./data/fifth_task.csv')
data.to_json('./data/fifth_task.json')

with open('./data/fifth_task.msgpack', 'wb') as f:
    f.write(msgpack.packb(data.to_dict()))

with open('./data/fifth_task.pkl', 'wb') as f:
    pickle.dump(data, f)

size_csv = os.path.getsize('./data/fifth_task.csv')
size_json = os.path.getsize('./data/fifth_task.json')
size_msgpack = os.path.getsize('./data/fifth_task.msgpack')
size_pkl = os.path.getsize('./data/fifth_task.pkl')
print(f'Размер файла fifth_task.csv: {size_csv} байт')
print(f'Размер файла fifth_task.json: {size_json} байт')
print(f'Размер файла fifth_task.msgpack: {size_msgpack} байт')
print(f'Размер файла fifth_task.pkl: {size_pkl} байт')
