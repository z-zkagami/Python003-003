# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = scrapy.Field()
    catagories = scrapy.Field()
    release_date = scrapy.Field()
