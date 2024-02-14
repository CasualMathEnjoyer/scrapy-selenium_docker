# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class RealityItem(scrapy.Item):
   number = scrapy.Field()
   title = scrapy.Field()
   imgurl = scrapy.Field()

class SeleniumScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
