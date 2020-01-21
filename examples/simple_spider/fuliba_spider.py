#!/usr/bin/env python

from ruia import Request, utils, AttrField, Item, Spider, TextField, Middleware

log = utils.log.get_logger()


fl_middleware = Middleware()


@fl_middleware.request
async def print_on_request(spider_ins, request):
    ua = 'ruia user-agent'
    request.headers.update({'User-Agent': ua})


class FulibaPageItem(Item):
    target_item = TextField(xpath_select='body/section/div[1]/div/article')
    title = TextField(xpath_select='header/h2/a')
    url = AttrField(xpath_select='header/h2/a', attr='href')


class HackerNewsSpider(Spider):
    start_urls = ['https://fulibus.net/']
    concurrency = 3

    async def parse(self, response):
        async for item in FulibaPageItem.get_items(html=response.html):
            yield item

    async def process_item(self, item):
        log.info("titem->{}".format({'url': item.url, 'title': item.title}))


if __name__ == "__main__":
    HackerNewsSpider.start(middleware=fl_middleware)
