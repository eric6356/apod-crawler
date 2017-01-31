import re
import logging
from datetime import datetime
from urllib.parse import urlparse

from apod.items import APODItem

logger = logging.getLogger(__name__)


class APODSpider(object):
    def parse_apod(self, response):
        apod = APODItem(whole_html=response.text, url=response.url)

        date = response.css('center:first-child>p:last-child::text').extract_first().strip()

        try:
            apod['date'] = datetime.strptime(date, '%Y %B %d')
        except ValueError:
            apod['date'] = datetime.strptime(date, '%B %d, %Y')

        apod['title'] = response.css('center:nth-child(2)>b:first-child::text').extract_first().strip()

        apod['explanation_html'] = response.css('body>p:first-of-type').extract_first()

        explanation = ''.join(one.extract() for one in response.css('body>p:first-of-type *::text'))
        explanation = re.sub(r'\n+', ' ', explanation).strip()
        if explanation.startswith('Explanation:'):
            explanation = explanation[len('Explanation:'):].strip()
        apod['explanation'] = explanation

        for a in response.css('a'):
            if a.css('img'):
                hd_img_url = response.urljoin(a.css('::attr("href")').extract_first())
                img_url = response.urljoin(a.css('img::attr("src")').extract_first())
                apod['img_path'] = urlparse(img_url).path
                apod['hd_img_path'] = urlparse(hd_img_url).path
                apod['file_urls'] = [hd_img_url, img_url]
                break
        else:
            logger.info('cannot find img in %s', response.url)

        yield apod
