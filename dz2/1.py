# Задание 1
# Загрузите матрицу из файла с форматом npy. Подсчитайте сумму всех элементов и их среднее арифметическое, подсчитайте сумму и среднее арифметическое главной и побочной диагоналей матрицы. Найдите максимальное и минимальное значение. Полученные значения запишите в json следующего формата:
# {
#     sum: 4,
#     avr: 4,
#     sumMD: 4, // главная диагональ
#     avrMD: 5,
#     sumSD: 4, // побочная диагональ
#     avrSD: 5,
#     max: 4,
#     min: 2
# }
#
# Исходную матрицу необходимо нормализовать и сохранить в формате npy.
import json
import numpy as np

matrix = np.load('./data/first_task.npy')

sum_all = np.sum(matrix)
avr_all = np.mean(matrix)
md = np.diagonal(matrix)
sum_md = np.sum(md)
avr_md = np.mean(md)
sd = np.diagonal(np.fliplr(matrix))
sum_sd = np.sum(sd)
avr_sd = np.mean(sd)
max_val = np.max(matrix)
min_val = np.min(matrix)

result = {
    'sum': float(sum_all),
    'avr': float(avr_all),
    'sumMD': float(sum_md),
    'avrMD': float(avr_md),
    'sumSD': float(sum_sd),
    'avrSD': float(avr_sd),
    'max': float(max_val),
    'min': float(min_val)
}

with open('./data/first_task.json', 'w') as f:
    json.dump(result, f)

norm_matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))

np.save('./data/first_task_normalized.npy', norm_matrix)

print(norm_matrix)
print(result)