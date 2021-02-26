import math
import scrapy


class BookSpider(scrapy.Spider):
    name = 'books'
    base_url = 'https://ilibrary.ru'
    start_urls = [

    ]
    count = 0

    def parse(self, response):
        index = math.ceil(BookSpider.count)
        file = open('pages/' + str(index) + '.txt', 'a', encoding='utf-8')

        for page in response.css('div.t.hya'):
            spans = page.css('span.p::text').getall()

            for span in spans:
                file.write(span)

        file.close()

        BookSpider.count += 0.5

        next_page = response.css('div.bnvin a:last-of-type::attr("href")').get()

        if next_page is not None:
            url = ''

            if index == 0:
                url = BookSpider.start_urls[0]
            elif index == BookSpider.count:
                url = BookSpider.base_url + next_page

            if len(url) > 0:
                index_file = open('index.txt', 'a')
                index_file.write(str(index) + ' ' + url + '\n')
                index_file.close()

            yield response.follow(next_page, self.parse)
