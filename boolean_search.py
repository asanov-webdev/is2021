import os
import pickle
from constants import PAGES_PATH

dict_file = open("inverted_index.pkl", "rb")
index_dict = pickle.load(dict_file)
dict_file.close()

print('Введите выражение с тремя логическими И, ИЛИ, НЕ:')

expression = input()
elements = expression.split(' ')
words = [elements[0], elements[2], elements[4]]
operations = [elements[1], elements[3]]

all_pages = []
pages = os.listdir(path=PAGES_PATH)

for i in range(len(pages)):
    all_pages.append(i)

index_arrays = []

for word in words:
    word = word.lower()

    if word[0] == '!':
        arr = list(set(all_pages) - set(index_dict.get(word[1:]).keys()))
    else:
        arr = index_dict.get(word).keys()

    index_arrays.append(arr)

if operations[0] == '&' and operations[1] == '&':
    search_result = list(set(index_arrays[0]) & set(index_arrays[1]) & set(index_arrays[2]))
elif operations[0] == '&' and operations[1] == '|':
    search_result = list(set(index_arrays[0]) & set(index_arrays[1]) | set(index_arrays[2]))
elif operations[0] == '|' and operations[1] == '&':
    search_result = list(set(index_arrays[0]) | set(index_arrays[1]) & set(index_arrays[2]))
elif operations[0] == '|' and operations[1] == '|':
    search_result = list(set(index_arrays[0]) | set(index_arrays[1]) | set(index_arrays[2]))

print(search_result)
