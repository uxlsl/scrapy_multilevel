# -*- coding: utf-8 -*-
import time
import scrapy


def walk(lst):
    if lst:
        i = lst.pop(0)
        yield i['url']
        yield from walk(i.get('extra'))
        yield from walk(lst)


class ZSpider(scrapy.Spider):
    name = 'z'
    allowed_domains = ['127.0.0.1']

    def start_requests(self):
        item = {'url':'http://127.0.0.1:5000/get?num=1',
                'extra':[
                    {'url': 'http://127.0.0.1:5000/get?num=2'},
                    {'url': 'http://127.0.0.1:5000/get?num=3', 'extra': [
                                                                        {'url': 'http://127.0.0.1:5000/get?num=5', 
                                                                         'extra': [{'url':'http://127.0.0.1:5000/get?num=6'}]}]},
                    {'url': 'http://127.0.0.1:5000/get?num=4'},
                    ]}
        req = scrapy.Request(url=item['url'], dont_filter=True)
        req.meta['w'] = walk(item['extra'])
        yield req
   
    def parse(self, response):
        w = response.meta['w']
        bodys = response.meta.get('bodys', '')
        #response = response.meta.get('responses', [])
        bodys += response.body_as_unicode()
        try:
            url = next(w)
            req = scrapy.Request(url=url, dont_filter=True)
            req.meta['bodys'] = bodys
            req.meta['w'] = w
            yield req
        except StopIteration as e:
            yield {'body': bodys}
