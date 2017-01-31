# -*- coding: utf-8 -*-
import scrapy

from apod.spiders import mixins


class LatestSpider(scrapy.Spider, mixins.APODSpider):
    name = "latest"
    allowed_domains = ["apod.nasa.gov"]
    start_urls = ['https://apod.nasa.gov/apod/astropix.html']

    def parse(self, response):
        return self.parse_apod(response)
