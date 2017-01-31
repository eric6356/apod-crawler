# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class APODMongoItem(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field(serializer=lambda d: d.strftime('%Y-%m-%d'))
    media_type = scrapy.Field()
    video_url = scrapy.Field()
    img_path = scrapy.Field()
    hd_img_path = scrapy.Field()
    explanation = scrapy.Field()
    explanation_html = scrapy.Field()
    whole_html = scrapy.Field()

    def __repr__(self):
        return str(self['url'])


class APODItem(APODMongoItem):

    file_urls = scrapy.Field()
    files = scrapy.Field()
