# -*- coding: utf-8 -*-
import scrapy

from apod.spiders import mixins


class ArchiveSpider(scrapy.Spider, mixins.APODSpider):
    name = 'archive'
    allowed_domains = ['apod.nasa.gov']
    start_urls = ['https://apod.nasa.gov/apod/archivepix.html']

    def parse(self, response):
        for i, href in enumerate(response.css('b a::attr("href")')):
            yield scrapy.Request(response.urljoin(href.extract()), callback=self.parse_apod)
