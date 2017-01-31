import re
import logging
from datetime import datetime
from urllib.parse import urlparse

from apod.items import APODItem

logger = logging.getLogger(__name__)


def parse_apod(response, apod):
    date = response.css('center:first-child>p:last-child::text').extract_first()

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
            apod['media_type'] = 'image'
            apod['img_path'] = urlparse(img_url).path
            apod['hd_img_path'] = urlparse(hd_img_url).path
            apod['file_urls'] = [hd_img_url, img_url]
            break
    else:
        logger.info('cannot find img in %s', response.url)
        apod['media_type'] = 'video'
        video_url = response.css('iframe::attr("src")').extract_first()
        if video_url is None:
            raise Exception('cannot find any media')
        apod['video_url'] = video_url

    yield apod


def parse_old_apod(response, apod):
    raise NotImplementedError()


class APODSpider(object):
    def parse_apod(self, response):
        apod = APODItem(whole_html=response.text, url=response.url)

        for parser in [parse_apod, parse_old_apod]:
            try:
                return parser(response, apod)
            except Exception as e:
                logger.info('%s can not be parsed, try next parser...', apod.url)
                logger.exception(e)

        logger.error('%s can not be parsed by any parser...', apod['url'])
        raise Exception('cannot parse {}'.format(apod['url']))
