# coding:utf-8
import scrapy
import logging
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from trademark.items import TrademarkItem
import json
import re
import time
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class JcsbSpider(CrawlSpider):
    name = "jcsb"

    start_urls = ['http://www.jcsb.com/search/1']

    rules = (
        Rule(LinkExtractor(allow='/search/\d+',), follow=True),
        Rule(LinkExtractor(allow='/goods/\d+.html'), callback='parse_item')
    )


    def parse_item(self,response):
        # 来源
        source = "精彩商标"
        # 来源地址
        source_url = response.url
        # 申请号
        application = ""

        # 商标名称
        name = response.xpath('//div[@class="title"]/h1/text()').extract()[0].replace("商标转让","").strip()
        # 类别
        category = re.findall('\d+',response.xpath('//p[@class="ss"]/a[2]/text()').extract()[0])[0]
        # 出售价
        price = ""
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = response.xpath('//div[@class="icc"]/p[5]/span[2]/text()').extract()[0].replace('初审公告期号：','')
        # 初审公告时间、
        bulletin_time = response.xpath('//div[@class="icc"]/p[6]/span[2]/text()').extract()[0]
        # 源网站对应标的图样
        image = response.xpath('//div[@class="left"]/img/@src').extract()[0]


        item = {}
        item['source'] = source
        item['source_url'] = source_url
        item['application'] = application
        item['name'] = name
        item['category'] = str(int(category))
        item['price'] = price
        item['contact_name'] = contact_name
        item['contact_phone'] = contact_phone
        item['bulletin_issue'] = bulletin_issue
        item['bulletin_time'] = bulletin_time
        item['image'] = image
        # with open('jcsb.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')

        yield item
