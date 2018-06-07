# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Tencent.items import PositionItem, TencentItem


class Tencent1Spider(CrawlSpider):
    name = 'tencent1'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=10']

    rules = (
        Rule(LinkExtractor(allow=r'position\.php\?&start=\d+'), callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d+'), callback='parse_position', follow=False),
    )

    def parse_page(self, response):
        url_list = response.xpath("//tr[@class='even']|//tr[@class='odd']")
        for url in url_list:
            item = TencentItem()
            item['position_name'] = url.xpath("./td[1]/a/text()").extract_first()
            item['position_link'] = 'https://hr.tencent.com/' + url.xpath("./td[1]/a/@href").extract_first()
            item['position_type'] = url.xpath("./td[2]/text()").extract_first()
            item['people_number'] = url.xpath("./td[3]/text()").extract_first()
            item['work_location'] = url.xpath("./td[4]/text()").extract_first()
            item['publish_times'] = url.xpath("./td[5]/text()").extract_first()

            yield item
            # yield scrapy.Request(item['position_link'],
            #                      # meta={"hello": item},
            #                      callback=self.parse_position)

    def parse_position(self, response):
        item = PositionItem()
        item['publish_zhize'] = "\n".join(
            response.xpath("//ul[@class='squareli']")[0].xpath("./li/text()").extract())
        item['publish_yaoqiu'] = "\n".join(
            response.xpath("//ul[@class='squareli']")[1].xpath("./li/text()").extract())
        # item数据交给管道处理
        yield item
