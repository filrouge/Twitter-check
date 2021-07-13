# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 12:16:21 2021

@author: ziadh
"""

import scrapy
from scrapy.crawler import CrawlerProcess

 
class QuotesSpider(scrapy.Spider):
    name = 'articles'

    start_urls = [
        'https://books.toscrape.com/',
    ]
    # get data
    def parse(self, response):
        for article in response.css('article.product_pod'):
            yield {
                'title': article.xpath('h3/a/@title').get(),
                'price': article.xpath('div/p/text()').get()[1::],
                'rating': article.css('p::attr(class)').get().split()[1],
                'availability': article.css('div p:nth-child(2)::attr(class)').get().split()[0],
                'image_url': 'https://books.toscrape.com/' + article.xpath('div/a/img/@src').get(),
            }


        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

# run spider
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'csv',      #ou jl, csv ....
    'FEED_URI': 'data.csv'     #ou .jl, .csv ....
    #definir un separateur '|'
    })
process.crawl(QuotesSpider)
process.start()


# run spider : scrapy runspider spider2.py -o Books.jl
# run spider : scrapy runspider spider2.py -o Books.json
# run spider : scrapy runspider spider2.py -o Books.csv