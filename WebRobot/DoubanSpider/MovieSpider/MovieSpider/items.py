# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviespiderItem(scrapy.Item):
    # define the fields for my item:
    title = scrapy.Field()
    rating = scrapy.Field()
    director = scrapy.Field()
    year = scrapy.Field()
