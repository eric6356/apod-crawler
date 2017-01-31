# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class APODBaseItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field(serializer=lambda d: d.strftime('%Y-%m-%d'))
    media_type = scrapy.Field()
    explanation = scrapy.Field()
    explanation_html = scrapy.Field()
    whole_html = scrapy.Field()

    def __repr__(self):
        return str(self['url'])


class APODIMageItem(APODBaseItem):
    img_path = scrapy.Field()
    hd_img_path = scrapy.Field()


class APODVideoItem(APODBaseItem):
    video_url = scrapy.Field()


class APODItem(APODIMageItem, APODVideoItem):
    file_urls = scrapy.Field()
    files = scrapy.Field()
