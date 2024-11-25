# Задание 4
# Считайте данные в формате pkl о товарах. Также считайте данные из файла формата json о новых ценах для каждого товара:
# {
#     name: "Apple",
#     method: "add"|"sub"|"percent+"|"percent-",
#     param: 4|0.01
# }
# Обновите цены для товаров в зависимости от метода:
# "add" – добавить значение param к цене;
# "sub" – отнять значение param от цены;
# "percent+" – поднять на param % (1% = 0.01);
# "percent-" – снизить на param %.
# Сохраните модифицированные данные обратно в формат pkl.
import json
import pickle

with open('./data/fourth_task_products.json', 'rb') as f:
    data = pickle.load(f)

print(data)
products_dict = {item['name']: item for item in data}

with open('./data/fourth_task_updates.json', 'r') as f:
    new_prices = json.load(f)

for update in new_prices:
    product = products_dict.get(update['name'])
    if product:
        if update['method'] == 'add':
            product['price'] += update['param']
        elif update['method'] == 'sub':
            product['price'] -= update['param']
        elif update['method'] == 'percent+':
            product['price'] *= 1 + update['param']
        elif update['method'] == 'percent-':
            product['price'] *= 1 - update['param']

with open('./data/fourth_task_modified.pkl', 'wb') as f:
    pickle.dump(data, f)

print(data)
