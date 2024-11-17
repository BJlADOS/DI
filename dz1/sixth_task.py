# Задание 6
# Найти публичный API, который возвращает JSON с некоторыми данными. Необходимо получить данные в формате JSON, преобразовать в html представление в зависимости от содержания.


import requests
from bs4 import BeautifulSoup

response = requests.get('https://jsonplaceholder.typicode.com/users')
data = response.json()

def json_to_html_table(json_data):
    soup = BeautifulSoup('<table></table>', 'html.parser')
    table = soup.table

    headers = json_data[0].keys()
    header_row = soup.new_tag('tr')
    for header in headers:
        th = soup.new_tag('th')
        th.string = header
        header_row.append(th)
    table.append(header_row)

    for item in json_data:
        row = soup.new_tag('tr')
        for header in headers:
            td = soup.new_tag('td')
            #decompose object to string
            itm = ''
            if isinstance(item[header], dict):
                itm = extract_json_deep(item[header])
            else:
                itm = str(item[header])
            td.string = itm
            row.append(td)
        table.append(row)

    return str(soup)

def extract_json_deep(json_object):
    values = []

    def extract_values(obj):
        if isinstance(obj, dict):
            for value in obj.values():
                extract_values(value)
        elif isinstance(obj, list):
            for item in obj:
                extract_values(item)
        else:
            values.append(str(obj))

    extract_values(json_object)
    return ' '.join(values)

html_table = json_to_html_table(data)
with open('data/sixth_task.html', 'w', encoding='utf-8') as file:
    file.write(html_table)
print(html_table)