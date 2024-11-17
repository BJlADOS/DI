import re
import pandas as pd

# Чтение HTML файла
with open('data/fifth_task.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Извлечение заголовков таблицы
header_pattern = re.compile(r'<th.*data-id="(.*)">(.*)</th>')
headers = header_pattern.findall(html_content)
data_ids = [header[0] for header in headers]
header_names = [header[1] for header in headers]

# Извлечение строк таблицы
row_pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
rows = row_pattern.findall(html_content)

# Извлечение данных из строк
data_pattern = re.compile(r'<td.*data-id="(.*)">(.*)</td>')
data = []
for row in rows[1:]: #Пропуск заголовка таблицы
    row_data = data_pattern.findall(row)
    row_dict = {cell[0]: cell[1] for cell in row_data}
    data.append(row_dict)

# Создание DataFrame
df = pd.DataFrame(data, columns=data_ids)

# Переименование столбцов
df.columns = header_names
df.to_csv('data/fifth_task_results.csv', index=False)

print(df)