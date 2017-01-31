# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging
from urllib.parse import urlparse

from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline

from apod.items import APODBaseItem, APODIMageItem, APODVideoItem

logger = logging.getLogger(__name__)


class APODMongoPipeline(object):
    collection_name = 'apod_item'
    media_dict = {
        'image': APODIMageItem,
        'video': APODVideoItem
    }

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection = self.db = self.client = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'apod')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if self.collection.find({'date': item['date']}).count():
            raise DropItem('{} already exists.'.format(item))

        item_class = self.media_dict.get(item['media_type'])
        if item_class is None:
            raise DropItem('unknown media type')

        item_mongo = item_class((f, item[f]) for f in item_class.fields)
        self.collection.insert(dict(item_mongo))

        return item


class APODFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        logger.debug('=' * 20)
        return urlparse(request.url).path
