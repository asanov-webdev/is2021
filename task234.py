import os
import pickle
from pymorphy2 import MorphAnalyzer, tokenizers
from constants import PAGES_PATH

morph = MorphAnalyzer()

inverted_index = {}
page_occurrences = {}

pages = os.listdir(path=PAGES_PATH)

for index, page in enumerate(pages):
    file = open(PAGES_PATH + page, 'r', encoding="utf-8")
    text = file.read()

    tokens = tokenizers.simple_word_tokenize(text)

    page_occurrences[index] = len(tokens)

    for token in tokens:
        lemma = morph.parse(token)[0].normal_form.lower()
        value = inverted_index.get(lemma)

        if value is None:
            inverted_index[lemma] = {index: 1}
        elif inverted_index[lemma].get(index) is None:
            inverted_index[lemma][index] = 1
        else:
            inverted_index[lemma][index] += 1

inverted_index_file = open("inverted_index.pkl", "wb")
pickle.dump(inverted_index, inverted_index_file)
inverted_index_file.close()

page_occurrences_file = open("page_occurrences.pkl", "wb")
pickle.dump(page_occurrences, page_occurrences_file)
page_occurrences_file.close()
