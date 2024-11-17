import re
import math

filename = 'data/third_task.txt'
results = []

def replace_na_with_avg(numbers):
    for i in range(len(numbers)):
        if numbers[i] == 'NA':
            left = numbers[i-1] if i > 0 else 0
            right = numbers[i+1] if i < len(numbers)-1 else 0
            numbers[i] = (left + right) / 2
    return numbers

with open(filename, 'r') as file:
    for line in file:
        nums = [float(num) if num != 'NA' else 'NA' for num in re.findall(r'NA|-?\d+', line)]
        nums = replace_na_with_avg(nums)
        filtered_nums = [num for num in nums if num > 0 and math.sqrt(num) < 200]
        results.append(sum(filtered_nums))

with open('data/third_task_result.txt', 'w') as file:
    for result in results:
        file.write(f'{result}\n')

print('Done!')