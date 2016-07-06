# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RmkickerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    spieler_name = scrapy.Field()
    spieler_note = scrapy.Field()
