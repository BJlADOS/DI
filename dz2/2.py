# Задание 2
# Загрузите матрицу из файла с форматом npy. Создайте три массива x y z. Отберите из матрицы значения, которые превышают следующее значение 501 следующим образом: индексы элемента разнесите по массивам x y, а само значение в массив z. Сохраните полученные массив в файл формата npz. Воспользуйтесь методами np.savez() и np.savez_compressed(). Сравните размеры полученных файлов.
import os
import numpy as np

matrix = np.load('./data/second_task.npy')

x, y, z = [], [], []
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i, j] > 501:
            x.append(i)
            y.append(j)
            z.append(matrix[i, j])

np.savez('./data/second_task.npz', x=x, y=y, z=z)
np.savez_compressed('./data/second_task_compressed.npz', x=x, y=y, z=z)

size = os.path.getsize('./data/second_task.npz')
size_compressed = os.path.getsize('./data/second_task_compressed.npz')

print(f'Размер файла second_task.npz: {size} байт')
print(f'Размер файла second_task_compressed.npz: {size_compressed} байт')