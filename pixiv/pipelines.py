# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.pipelines.images import ImagesPipeline, DropItem


class PixivPipeline(ImagesPipeline):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Host': '',
        'Referer': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36',
    }

    def file_path(self, request, response=None, info=None):
        url = request.url
        id = re.search(r'/(\d+)_p', url).groups()[0]
        fn = 'pixiv_%s.jpg' % id
        return fn

    def get_media_requests(self, item, info):
        return scrapy.Request(item['url'], headers=self.headers)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths or len(image_paths) != 1:
            raise DropItem("Item contains no images")
        return item
