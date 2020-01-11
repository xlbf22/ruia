#!/usr/bin/env python

from ruia import Request, Spider, utils, Item, Middleware, AttrField, TextField

log = utils.log.get_logger()

fl_middleware = Middleware()


@fl_middleware.request
async def print_on_request(spider_ins, request):
    ua = 'ruia user-agent'
    request.headers.update({'User-Agent': ua})


class CaoliuPageItem(Item):
    target_item = TextField(xpath_select='//*/tr[@align="center"][not(@onmouseover)][position()>10]')
    title = TextField(xpath_select='td[2]/a')
    url = AttrField(xpath_select='td[2]/a', attr='href')


class HackerNewsSpider(Spider):
    start_urls = ['http://test2048.net/2048/thread.php?fid-24.html']
    concurrency = 3

    async def parse(self, response):
        for index, url in enumerate(self.start_urls):
            yield Request(url, callback=self.parse_item, metadata={'index': index})

    async def parse_item(self, response):
        async for item in CaoliuPageItem.get_items(html=response.html):
            yield item

    async def process_item(self, item):
        log.info("titem->{}".format({'url': item.url, 'title': item.title}))


if __name__ == "__main__":
    HackerNewsSpider.start(middleware=fl_middleware)
