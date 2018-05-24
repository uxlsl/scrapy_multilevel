# -*- coding: utf-8 -*-
import time
import scrapy


def walk(lst, levels):
    if lst:
        i = lst.pop(0)
        yield i['url']
        levels[0] += 1
        yield from walk(i.get('extra'), levels)
        levels[0] -= 1
        yield from walk(lst, levels)


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
        levels = [0]
        req.meta['w'] = walk(item['extra'], levels)
        req.meta['levels'] = levels
        yield req
   
    def parse(self, response):
        w = response.meta['w']
        bodys = response.meta.get('bodys', '')
        responses = response.meta.get('responses', [])
        print(responses)
        bodys += response.body_as_unicode()
        try:
            levels = response.meta['levels']
            level = levels[0]
            url = next(w)
            if level < levels[0]:
                responses.append(response)
            elif level > levels[0]:
                responses.pop()
            req = scrapy.Request(url=url, dont_filter=True)
            req.meta['responses'] = responses
            req.meta['bodys'] = bodys
            req.meta['w'] = w
            req.meta['levels'] = levels
            yield req
        except StopIteration as e:
            yield {'body': bodys}
