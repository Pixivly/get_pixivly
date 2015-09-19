import re
import os
import json
from datetime import datetime, timedelta
import scrapy
from scrapy.http import Request
from pixiv.items import PixivItem
from pixiv.settings import PAGE, JSONS_STORE, IMAGES_STORE


class PixivSpider(scrapy.Spider):
    """
        Spider for daily top illustrations on Pixiv
    """
    name = 'pixiv'
    allowed_domains = ['pixiv.net']
    url_pattern = 'http://www.pixiv.net/ranking.php?mode=daily&content=illust&format=json&date={0}&p={1}'

    def __init__(self, start=None, end=None, *args, **kwargs):
        super(PixivSpider, self).__init__(*args, **kwargs)
        if start is None or start == 'today':
            start = datetime.today().date().strftime('%Y%m%d')
        if end is None:
            end = '20100101'
        try:
            self.start_date = datetime.strptime(start, '%Y%m%d').date()
            self.end_date = datetime.strptime(end, '%Y%m%d').date()
        except ValueError:
            raise ValueError('%s or %s is not a valid date' % (start, end))
        if self.start_date < self.end_date:
            raise ValueError('%s must smaller than %s' % (self.end_date, self.start_date))

    def start_requests(self):
        dt = timedelta(1)
        date = self.start_date
        # every day
        while date != self.end_date:
            for p in range(1, PAGE+1):
                url = self.url_pattern.format(date.strftime('%Y%m%d'), p)
                yield Request(url)
            date = date - dt

    def parse(self, response):
        jsondata = json.loads(response.body)
        p = re.search(r'p=(\d+)', response.url).groups()[0]
        file = os.path.join(JSONS_STORE, '%s_%02d.json'%(jsondata['date'], int(p)))
        with open(file, 'w') as fd:
            json.dump(jsondata, fd)
        for illust in jsondata['contents']:
            item = PixivItem()
            item['id'] = illust['illust_id']
            item['url'] = illust['url']
            file = os.path.join(IMAGES_STORE, 'pixiv_%s.jpg'%item['id'])
            if not os.path.exists(file):
                yield item
