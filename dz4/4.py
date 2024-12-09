# Задание 4
# Дан набор файлов. В одних содержится информация о некоторых товарах, которые нужно сохранить в соответствующей таблице базы данных. В других (начинающихся с префикса upd) содержится информация об изменениях, которые могут задаваться разными командами: изменение цены, изменение остатков, снять/возврат продажи, удаление из каталога (таблицы). По одному товару могут быть несколько изменений, поэтому при создании таблицы необходимо предусмотреть поле-счетчик, которое инкрементируется каждый раз, когда происходит обновление строки. Все изменения необходимо производить, используя транзакции, проверяя изменения на корректность (например, цена или остатки после обновления не могут быть отрицательными)
# После записи всех данные и применения обновлений необходимо выполнить следующие запросы:
# 	вывести топ-10 самых обновляемых товаров
# 	проанализировать цены товаров, найдя (сумму, мин, макс, среднее) для каждой группы, а также количество товаров в группе
# 	проанализировать остатки товаров, найдя (сумму, мин, макс, среднее) для каждой группы товаров
# 	произвольный запрос

import sqlite3
import pandas as pd
import msgpack

conn = sqlite3.connect('fourth_task_products.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    quantity INTEGER,
    category TEXT,
    fromCity TEXT,
    isAvailable BOOLEAN,
    views INTEGER,
    update_count INTEGER DEFAULT 0
)
''')
conn.commit()

with open('./data/4/_product_data.text', 'r', encoding='utf-8') as file:
    data = file.read().split('=====')
    for item in data:
        if item.strip():
            product = {}
            for line in item.strip().split('\n'):
                key, value = line.split('::')
                product[key.strip()] = value.strip()
            cursor.execute('''
            INSERT INTO products (name, price, quantity, category, fromCity, isAvailable, views)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (product.get('name'), float(product.get('price')), int(product.get('quantity')),
                  product.get('category'), product.get('fromCity'), product.get('isAvailable') == 'True',
                  int(product.get('views'))))
conn.commit()

with open('./data/4/_update_data.msgpack', 'rb') as file:
    updates = msgpack.unpack(file, raw=False)
    for update in updates:
        cursor.execute('BEGIN TRANSACTION')
        try:
            if update['method'] == 'update_price':
                new_price = update['param']
                if new_price < 0:
                    raise ValueError("Цена не может быть отрицательной")
                cursor.execute('''
                UPDATE products SET price = ?, update_count = update_count + 1 WHERE name = ?
                ''', (new_price, update['name']))
            elif update['method'] == 'update_quantity':
                new_quantity = update['param']
                if new_quantity < 0:
                    raise ValueError("Количество не может быть отрицательным")
                cursor.execute('''
                UPDATE products SET quantity = ?, update_count = update_count + 1 WHERE name = ?
                ''', (new_quantity, update['name']))
            elif update['method'] == 'remove_product':
                cursor.execute('''
                DELETE FROM products WHERE name = ?
                ''', (update['name'],))
            elif update['method'] == 'available':
                cursor.execute('''
                UPDATE products SET isAvailable = ?, update_count = update_count + 1 WHERE name = ?
                ''', (update['param'], update['name']))
            elif update['method'] == 'quantity_sub':
                cursor.execute('''
                SELECT quantity FROM products WHERE name = ?
                ''', (update['name'],))
                current_quantity = cursor.fetchone()[0]
                new_quantity = current_quantity - update['param']
                if new_quantity < 0:
                    raise ValueError("Количество не может быть отрицательным")
                cursor.execute('''
                UPDATE products SET quantity = ?, update_count = update_count + 1 WHERE name = ?
                ''', (new_quantity, update['name']))
            elif update['method'] == 'price_percent':
                cursor.execute('''
                SELECT price FROM products WHERE name = ?
                ''', (update['name'],))
                current_price = cursor.fetchone()[0]
                new_price = current_price * (1 + update['param'] / 100.0)
                if new_price < 0:
                    raise ValueError("Цена не может быть отрицательной")
                cursor.execute('''
                UPDATE products SET price = ?, update_count = update_count + 1 WHERE name = ?
                ''', (new_price, update['name']))
            elif update['method'] == 'price_abs':
                cursor.execute('''
                SELECT price FROM products WHERE name = ?
                ''', (update['name'],))
                current_price = cursor.fetchone()[0]
                new_price = current_price + update['param']
                if new_price < 0:
                    raise ValueError("Цена не может быть отрицательной")
                cursor.execute('''
                UPDATE products SET price = ?, update_count = update_count + 1 WHERE name = ?
                ''', (new_price, update['name']))
            elif update['method'] == 'quantity_add':
                cursor.execute('''
                SELECT quantity FROM products WHERE name = ?
                ''', (update['name'],))
                current_quantity = cursor.fetchone()[0]
                new_quantity = current_quantity + update['param']
                if new_quantity < 0:
                    raise ValueError("Количество не может быть отрицательным")
                cursor.execute('''
                UPDATE products SET quantity = ?, update_count = update_count + 1 WHERE name = ?
                ''', (new_quantity, update['name']))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error applying update: {e}")

top_10_updated = pd.read_sql('''
SELECT name, update_count FROM products ORDER BY update_count DESC LIMIT 10
''', conn)
print(top_10_updated)

price_analysis = pd.read_sql('''
SELECT category, SUM(price) as total_price, MIN(price) as min_price, MAX(price) as max_price, AVG(price) as avg_price, COUNT(*) as product_count
FROM products GROUP BY category
''', conn)
print(price_analysis)

quantity_analysis = pd.read_sql('''
SELECT category, SUM(quantity) as total_quantity, MIN(quantity) as min_quantity, MAX(quantity) as max_quantity, AVG(quantity) as avg_quantity
FROM products GROUP BY category
''', conn)
print(quantity_analysis)

available_products = pd.read_sql('''
SELECT * FROM products WHERE isAvailable = 1
''', conn)
print(available_products)

conn.close()