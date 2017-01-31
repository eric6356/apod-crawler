# -*- coding: utf-8 -*-
import scrapy


class IndexSpider(scrapy.Spider):
    name = "index"
    allowed_domains = ["apod.nasa.gov"]
    start_urls = ['https://apod.nasa.gov/apod/lib/aptree.html']

    # TODO.
    def parse(self, response):
        pass
