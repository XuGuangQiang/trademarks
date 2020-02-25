# coding:utf-8
import scrapy
import logging
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from trademark.items import TrademarkItem

import json
import re
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class ZanBiaoSpider(CrawlSpider):
    name = "zanbiao"

    # start_urls = ['http://www.zbtm88.com/product/']

    rules = (
        Rule(LinkExtractor(allow='-\d+.html',),  callback='parse_page', follow=True),
    )

    def start_requests(self):
        url = "http://www.zbtm88.com/product/"
        yield scrapy.Request(url=url,callback=self.parse_type)

    def parse_type(self,response):
        urls = response.xpath('//div[@class="div_columns"]/ul/li/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url)

    def parse_page(self, response):
        urls = response.xpath('//div[@class="right_1"]/ul/li/h6/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url,callback=self.parse_item)

    def parse_item(self,response):
        # 来源
        source = "赞标"
        # 来源地址
        source_url = response.url
        # 申请号
        application = response.xpath('//ul[@class="ul_1"]/li[3]/span/text()').extract()[0]
        # 商标名称
        name = response.xpath('//title/text()').extract()[0].split('-')[1].strip()
        # 类别
        category = int(re.findall('\d+',response.xpath('//title/text()').extract()[0].split('-')[0])[0])
        # 出售价
        price = ""
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = ""
        # 初审公告时间、
        bulletin_time = ""
        # 源网站对应标的图样
        image = response.xpath('//div[@class="propic"]/img/@src').extract()[0]
        if "http" not in image:
            image = "http://www.zbtm88.com/" + image

        item = {}
        item['source'] = source
        item['source_url'] = source_url
        item['application'] = application
        item['name'] = name
        item['category'] = str(category)
        item['price'] = price
        item['contact_name'] = contact_name
        item['contact_phone'] = contact_phone
        item['bulletin_issue'] = bulletin_issue
        item['bulletin_time'] = bulletin_time
        item['image'] = image
        # with open('zanbiao.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')

        yield item
