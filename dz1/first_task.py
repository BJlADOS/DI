import re
import collections

#without defs
filename = 'data/first_task.txt'
vowels = 'aeiouy'
words = []
words_vowels = []
words_vowels_count = 0
words_count = 0

with open(filename, 'r') as file:
    for line in file:
        words += re.findall(r'\b\w+\b', line.lower())
    words_count += len(words)
    words_vowels += [word for word in words if word[0] in vowels]
    words_vowels_count += len(words_vowels)

words_freq = collections.Counter(words)
words_freq = dict(sorted(words_freq.items(), key=lambda item: item[1], reverse=True))

with open('data/first_task_result.txt', 'w') as file:
    for word, freq in words_freq.items():
        file.write(f'{word}:{freq}\n')
    file.write('-----------\n')
    file.write(f'Words count: {words_count}\n')
    file.write(f'Words vowels count: {words_vowels_count}\n')
    file.write(f'Words vowels ratio: {words_vowels_count / words_count}\n')

print('Done!')
