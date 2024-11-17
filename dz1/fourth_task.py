import pandas as pd

# Чтение CSV файла
df = pd.read_csv('data/fourth_task.txt')

# Удаление столбца expiration_date
df.drop(columns=['expiration_date'], inplace=True)

# Вычисление среднего арифметического по столбцу rating
mean_rating = df['rating'].mean()

# Вычисление максимума по столбцу price
max_price = df['price'].max()

# Вычисление минимума по столбцу rating
min_rating = df['rating'].min()

# Фильтрация строк, где status равен Available for Pickup
filtered_df = df[df['status'] == 'Available for Pickup']

# Запись результатов поиска значений в отдельный файл
with open('data/fourth_task_results.txt', 'w') as file:
    file.write(f'{mean_rating}\n')
    file.write(f'{max_price}\n')
    file.write(f'{min_rating}\n')

# Запись модифицированного CSV файла в отдельный файл
filtered_df.to_csv('data/fourth_task_results_table.csv', index=False)

print('Done!')