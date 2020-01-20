#!/usr/bin/env python

from ruia import Spider, utils, Item, Middleware, AttrField, TextField
from ruia_pyppeteer import PyppeteerRequest as Request

log = utils.log.get_logger()

fl_middleware = Middleware()


@fl_middleware.request
async def print_on_request(spider_ins, request):
    # ua = 'ruia user-agent'
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    request.headers.update({'User-Agent': ua})


# class HitomiImageItem(Item):
#     target_item = TextField(xpath_select='//*[@id="comicImages"]')
#     url = AttrField(xpath_select='img', attr='src')
#
#
# class HitomiImageSpider(Spider):
#     # start_urls = ['https://hitomi.la/cg/theevilwithin-kidman-恶灵附身-基德曼-中文-1426580.html']
#     concurrency = 3
#
#     async def parse(self, response):
#         for index, url in enumerate(self.start_urls):
#             yield Request(url, callback=self.parse_item, metadata={'index': index})
#
#     async def parse_item(self, response):
#         async for item in HitomiImageItem.get_items(html=response.html):
#             yield item
#
#     async def process_item(self, item):
#         log.info("titem->{}".format({'url': item.url, 'title': item.title}))
#
#
class HitomiPageItem(Item):
    # target_item = TextField(xpath_select='//*/div/div[2]/div[4]/div[2]/ul/li')
    # url = AttrField(xpath_select='div/a', attr='href')
    target_item = TextField(xpath_select='//body')
    url = AttrField(xpath_select='div[@id="comicImages"]/img', attr='src')


class HitomiPageSpider(Spider):
    b_url = 'https://hitomi.la/reader/1426580.html'
    # start_urls = ['https://hitomi.la/cg/theevilwithin-kidman-恶灵附身-基德曼-中文-1426580.html']
    # start_urls = [b_url+'#1', b_url+'#2', b_url+'#3', b_url+'#4', b_url+'#5', b_url+'#6', b_url+'#7', b_url+'#8', b_url+'#9', b_url+'#10', b_url+'#11', b_url+'#12', b_url+'#13', b_url+'#14', b_url+'#15', b_url+'#16', b_url+'#17', b_url+'#18', b_url+'#19', b_url+'#20', b_url+'#21', b_url+'#22', b_url+'#23']
    start_urls = [b_url+'#1']
    concurrency = 3

    async def parse(self, response):
        for index, url in enumerate(self.start_urls):
            # yield Request(url, callback=self.parse_item, metadata={'index': index})
            yield Request(url, callback=self.parse_item, load_js=True, metadata={'index': index}).fetch()

    async def parse_item(self, response):
        log.info("html->[{}]".format(response.html))
        if response.html != '':
            async for item in HitomiPageItem.get_items(html=response.html):
                yield item

    async def process_item(self, item):
        log.info("titem->{}".format(item))
        # HitomiImageSpider.start_urls = [item.url]
        # HitomiImageSpider.start(middleware=fl_middleware)


if __name__ == "__main__":
    HitomiPageSpider.start(middleware=fl_middleware)
