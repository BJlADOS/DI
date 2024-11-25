# Задание 3
# Считайте массив объектов в формате json. Агрегируйте информацию по каждому товару, получив следующую информацию: средняя цена, максимальная цена, минимальная цена. Сохранить полученную информацию по каждому объекту в формате json, а также в формате msgpack. Сравните размеры полученных файлов.

import json
import msgpack
import numpy as np
import os

with open('./data/third_task.json', 'r') as f:
    data = json.load(f)

result = []
prices = [item['price'] for item in data]
avg_price = np.mean(prices)
max_price = np.max(prices)
min_price = np.min(prices)
result.append({
    'avg_price': float(avg_price),
    'max_price': float(max_price),
    'min_price': float(min_price)
})

with open('./data/third_task_result.json', 'w') as f:
    json.dump(result, f)

with open('./data/third_task.msgpack', 'wb') as f:
    f.write(msgpack.packb(result))

size = os.path.getsize('./data/third_task_result.json')
size_msgpack = os.path.getsize('./data/third_task.msgpack')

print(f'Размер файла third_task.json: {size} байт')
print(f'Размер файла third_task.msgpack: {size_msgpack} байт')
