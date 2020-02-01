#!/usr/bin/env python

from ruia import Request, Spider, utils, Item, Middleware, AttrField, TextField
import re, os, urllib, datetime, socket

socket.setdefaulttimeout(15)

log = utils.log.get_logger()

fl_middleware = Middleware()

str_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')

base_url = '''http://test2048.net/2048/'''
base_path = '''/Users/mpauli/Desktop/caoliu'''
ua = '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'''

@fl_middleware.request
async def print_on_request(spider_ins, request):
    # ua = 'ruia user-agent'
    request.headers.update({'User-Agent': ua})


class CaoliuPageItem(Item):
    target_item = TextField(xpath_select='//div[9]/table//tr[position()>10 and position()<55]/td[2]', default='')
    title = TextField(xpath_select='./a', default='')
    url = AttrField(xpath_select='./a', attr='href', default='')


class CaoliuBodyItem(Item):
    target_item = TextField(xpath_select='//*[@id="read_tpc"]/img', default='')
    title = TextField(xpath_select='//*[@id="subject_tpc"]', default='')
    url = AttrField(xpath_select='.', attr='src', default='')
    index = 0


class CaoliuSpider(Spider):
    start_urls = [base_url+'thread.php?fid-24.html']
    concurrency = 3

    async def parse(self, response):
        log.info("parse 0")
        index = 0
        async for item in CaoliuPageItem.get_items(html=response.html):
            index += 1
            # if index > 1:
            #     return
            log.info("item.url={}".format(item.url))
            yield Request(base_url+item.url, callback=self.parse_item)

    async def parse_item(self, response):
        log.info("parse 1")
        index = 0
        async for item in CaoliuBodyItem.get_items(html=response.html):
            index += 1
            item.index = index
            yield item

    async def process_item(self, item):
        # log.info("titem: {}".format(item))
        dirname = re.sub('[\/:*?"<>|]', '-', item.title)
        path = base_path + '/[' + str_date + ']' + dirname
        if not os.path.exists(path):
            os.makedirs(path)
        filename = path+('/image%03d.' % item.index)+item.url.split(".")[-1]
        log.info("{}".format({'filename': filename, 'url': item.url}))
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', ua)]
        try:
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(item.url, filename=filename)
        except Exception as ex:
            log.error("url->{}\n{}".format(item.url, ex))


if __name__ == "__main__":
    CaoliuSpider.start(middleware=fl_middleware)
