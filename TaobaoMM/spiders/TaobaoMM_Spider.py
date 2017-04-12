from scrapy.spiders import Spider
from TaobaoMM.items import TaobaommItem
import json
from scrapy.http import Request
from TaobaoMM.pipelines import TaobaommPipeline

class TaobaoMMSpider(Spider):
    name = 'taobaomm'
    allowed_domains = ['mm.taobao.com']
    start_urls = [
        "https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8"
    ]


    def parse(self, response):
        html = json.loads(response.text)
        status = html["status"]


        if status == -1:
            print(u"Crawled the end")

        else:
            searchDOList = html["data"]["searchDOList"]
            currentPage = html["data"]["currentPage"]
            for i in searchDOList:
                items = TaobaommItem()
                items = i
                yield items

            print(u"The Page " + str(currentPage) + u" Crawled: <" + str(response.status) + " " + response.url + " >")

            next_url = "https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8&currentPage=%s" % str(currentPage+1)
            yield Request(url=next_url, callback=self.parse)
