import numpy as np
import os
import pickle
from pymorphy2 import MorphAnalyzer
from constants import PAGES_PATH

morph = MorphAnalyzer()

inverted_index_file = open("inverted_index.pkl", "rb")
inverted_index = pickle.load(inverted_index_file)
inverted_index_file.close()

pages = os.listdir(path=PAGES_PATH)
words = inverted_index.keys()

index_txt_dict = {}
index_txt_file = open('./scrapyproject/index.txt')

for line in index_txt_file:
    i = line.split(' ')[0]
    url = line.split(' ')[1][:-1]

    index_txt_dict[int(i)] = url

index_txt_file.close()


def save_all_vectors():
    vectors = []

    for i in range(len(pages)):
        vector = []

        for word in words:
            val = inverted_index.get(word).get(i)

            if val is None:
                vector.append(0)
            else:
                vector.append(val)

        vectors.append(vector)

    with open('all_vectors.txt', 'wb') as fp:
        pickle.dump(vectors, fp)


def get_query_vector():
    vector = []
    word_positions = []

    for i, word in enumerate(words):
        if word in query_words:
            word_positions.append(i)

    for i in range(len(words)):
        if i in word_positions:
            vector.append(1)
        else:
            vector.append(0)

    return vector


def get_vectors_cos(v1, v2):
    np_vector1 = np.array(v1)
    np_vector2 = np.array(v2)

    dot_product = np.dot(np_vector1, np_vector2)
    norm1 = np.linalg.norm(np_vector1)
    norm2 = np.linalg.norm(np_vector2)

    cos = dot_product / (norm1 * norm2)

    return cos


with open('all_vectors.txt', 'rb') as fp:
    all_vectors = pickle.load(fp)

print('Введите поисковый запрос:')

query = input()

query_words = query.split(' ')

for i in range(len(query_words)):
    query_words[i] = morph.parse(query_words[i])[0].normal_form.lower()

query_vector = get_query_vector()

cos_dict = {}

for i, v in enumerate(all_vectors):
    cos = get_vectors_cos(v, query_vector)
    cos_dict[i] = cos

sorted_dict = {r: cos_dict[r] for r in sorted(cos_dict, key=cos_dict.get, reverse=True)}

for key in list(sorted_dict.keys())[:5]:
    print(index_txt_dict.get(key))
