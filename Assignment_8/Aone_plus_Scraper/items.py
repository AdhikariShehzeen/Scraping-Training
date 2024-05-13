# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AonePlusScraperItem(scrapy.Item):
    # define the fields for your item here like:
    Name = scrapy.Field()
    Price = scrapy.Field()
    URL = scrapy.Field()
    pass
