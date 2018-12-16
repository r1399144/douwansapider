# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouwanGifItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    PaperName =  scrapy.Field()
    Tatile = scrapy.Field()
    Context = scrapy.Field()
    GifLink = scrapy.Field()
    pass
class DouwanPaperItem(scrapy.Item):
    # define the fields for your item here like:
    PaperName =  scrapy.Field()
    PaperLink = scrapy.Field()
    pass
