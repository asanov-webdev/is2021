import math
import os
import pickle
import plotly.graph_objects as go
from constants import PAGES_PATH

inverted_index_file = open("inverted_index.pkl", "rb")
inverted_index = pickle.load(inverted_index_file)
inverted_index_file.close()

page_occurrences_file = open("page_occurrences.pkl", "rb")
page_occurrences = pickle.load(page_occurrences_file)
page_occurrences_file.close()

pages = os.listdir(path=PAGES_PATH)

tf_values = []
idf_values = []
tf_idf_values = []


def toFixed(numObj, digits=0):
    return float(f"{numObj:.{digits}f}")


def get_tfs(word):
    tfs = []

    for i in range(len(pages)):
        value = inverted_index.get(word).get(i)

        if value is None:
            tfs.append(0)
        else:
            tfs.append(toFixed(value / page_occurrences.get(i), 5))

    tf_values.append(tfs)


def get_idf(word):
    numerator = len(pages)
    denominator = len(inverted_index.get(word).keys())

    idf = toFixed(math.log10(numerator / denominator), 5)

    idf_values.append(idf)


def get_tf_idfs(i):
    tf_idfs = []
    tfs = tf_values[i]

    for tf in tfs:
        tf_idf = tf * idf_values[i]
        tf_idfs.append(toFixed(tf_idf, 5))

    tf_idf_values.append(tf_idfs)


words = inverted_index.keys()

for i, word in enumerate(words):
    get_tfs(word)
    get_idf(word)
    get_tf_idfs(i)


def show_idf():
    fig = go.Figure(data=[go.Table(header=dict(values=['Words', 'IDF']),
                                   cells=dict(values=[list(words), list(idf_values)]))
                          ])
    fig.show()


def show_tf():
    fig = go.Figure(data=[go.Table(header=dict(values=list(words)[:10]),
                                   cells=dict(values=list(tf_values)[:10]))
                          ])
    fig.show()


def show_tf_idf():
    fig = go.Figure(data=[go.Table(header=dict(values=list(words)[:10]),
                                   cells=dict(values=list(tf_idf_values)[:10]))
                          ])
    fig.show()


show_tf()
show_idf()
show_tf_idf()
