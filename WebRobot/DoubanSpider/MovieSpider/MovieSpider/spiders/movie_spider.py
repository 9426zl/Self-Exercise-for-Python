import re
import scrapy
from MovieSpider.items import MoviespiderItem


class Moviespider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = [
        "http://www.douban.com/doulist/13712700/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = MoviespiderItem()
            item['title'] = sel.xpath('//a[contains(@href,"subject")]/text()').re('\s+(\S+.*)\s+')
            item['rating'] = sel.xpath('//span[contains(@class,"rating_nums")]/text()').re('(\d+\.\d+)')
            item['director'] = sel.xpath('//div[contains(@class,"abstract")]/text()').re(u'\s+\u5bfc\u6f14:(.*)\s+')
            item['year'] = sel.xpath('//div[contains(@class,"abstract")]/text()').re(u'\s+\u5e74\u4efd:(.*)\s+')
            yield item