# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy,re
from scrapy.loader.processors import MapCompose,TakeFirst,Join


class VideoEastdayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    video_url = scrapy.Field()
    video_title = scrapy.Field()
    video_local_path = scrapy.Field()
