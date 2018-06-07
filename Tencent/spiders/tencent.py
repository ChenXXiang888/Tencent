# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem, PositionItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    # offset = 0
    # base_urls = 'https://hr.tencent.com/position.php?&start='
    # start_urls = [base_urls + str(offset)]  # 字符串拼接
    # 方法三
    base_urls = 'https://hr.tencent.com/position.php?&start='
    start_urls = [base_urls + str(page) for page in range(0, 3771, 10)]  # 字符串拼接

    def parse(self, response):
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
            yield scrapy.Request(item['position_link'],
                                 # meta={"hello": item},
                                 callback=self.parse_page)

    def parse_page(self, response):
        item = PositionItem()
        item['publish_zhize'] = "\n".join(
            response.xpath("//ul[@class='squareli']")[0].xpath("./li/text()").extract())
        item['publish_yaoqiu'] = "\n".join(
            response.xpath("//ul[@class='squareli']")[1].xpath("./li/text()").extract())
        # item数据交给管道处理
        yield item
        # 方法一
        # if self.offset < 3830:
        #     self.offset += 10
        #     url = self.base_urls + str(self.offset)
        # request数据交给调试器处理(框架已经实现)
        # yield scrapy.Request(url, callback=self.parse)
        # 方法二 一直取下一页
        # //a[@class='noactive' and @id='next']  用时1分50秒
        # 如果
        # if not response.xpath("//a[@class='noactive' and @id='next']").extract_first():
        #    next_url = 'https://hr.tencent.com/' +response.xpath("//a[@id='next']/@href").extract_first()
        #    yield scrapy.Request(next_url, callback=self.parse)
        # 方法三  通过start_urls构建所有的url地址
