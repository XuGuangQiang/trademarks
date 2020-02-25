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
from tools import tg


class TuiGuaSpider(CrawlSpider):
    name = "tuigua"
    # start_urls = tg()
    start_urls = ['https://www.tuigua.com/trade/list']

    rules = (
        Rule(LinkExtractor(allow='\?cate_id=\d+'),follow=True),
        Rule(LinkExtractor(allow='&page=\d+',), follow=True),
        Rule(LinkExtractor(allow='/detail/\d+.html'), callback='parse_item'),
    )


    def parse_item(self,response):
        # 来源
        source = "推瓜"
        # 来源地址    
        source_url = response.url
        # 申请号
        application = ""
        # 商标名称
        name = response.xpath('//meta[@name="keywords"]/@content').extract()[0].replace(" 商标转让","").strip()
        # 类别
        category = response.xpath('//div[@class="pline floatpline"][1]/p/span/text()').extract()[0].split('-')[0].replace('第','').replace('类','')
        # 出售价
        price = response.xpath('//div[@class="pline floatpline"][3]/p/span/span/text()').extract()[0]
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        try:
            bulletin_issue = response.xpath('//ul[@class="traded1"]/li[1]/p[2]/text()').extract()[0].replace('无','').strip()
        except:
            bulletin_issue = ""
        # 初审公告时间、
        try:
            bulletin_time = response.xpath('//ul[@class="traded1"]/li[2]/p[2]/text()').extract()[0].replace('无','').strip()
        except:
            bulletin_time = ""
        # 源网站对应标的图样
        image = response.xpath('//div[@class="detailtlbox"]/img/@src').extract()[0]
        if "http" not in image:
            image = "https:" + image

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
        # with open('tuigua_goods.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')

        yield item
