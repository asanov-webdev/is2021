import os
import sys


def add_url():
    f = open(path, "r")
    contents = f.readlines()
    f.close()

    contents.insert(8, '\t\t\'' + page_url + '\'')

    f = open(path, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()


LINE_INDEX = 8

page_url = sys.argv[1]

path = './scrapyproject/scrapyproject/spiders/book_spider.py'

command = 'cd scrapyproject && scrapy crawl books'

if __name__ == '__main__':
    add_url()

    os.system(command)
