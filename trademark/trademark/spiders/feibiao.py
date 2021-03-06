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



class FeiBiaoSpider(CrawlSpider):
    name = "feibiao"

    start_urls = ['https://www.ipfeibiao.com/deal_tm/l1']

    rules = (
        Rule(LinkExtractor(allow='deal_tm/l\d+',), follow=True),
        Rule(LinkExtractor(allow='view/\d+.html'), callback='parse_item'),
    )


    def parse_item(self,response):
        # 来源
        source = "飞镖"
        # 来源地址    
        source_url = response.url
        # 申请号
        application = response.xpath('//div[@class="tit_goods"]/h1/span[2]/text()').extract()[0]
        # 商标名称
        name = response.xpath('//div[@class="tit_goods"]/h1/span[3]/text()').extract()[0].replace(" 商标转让","").strip()
        # 类别
        category = response.xpath('//div[@class="tit_goods"]/h1/span[1]/text()').extract()[0].split('-')[0].replace('第','').replace('类','').replace('\t','')
        # 出售价
        price = response.xpath('//div[@class="price"]/span/text()').extract()[0]
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = ""
        # 初审公告时间、
        bulletin_time = ""
        # 源网站对应标的图样
        image = response.xpath('//div[@id="demo"]/img/@src').extract()[0]
        if "http" not in image:
            image = "https://www.ipfeibiao.com" + image

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
        # with open('feibiao_goods.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')


        yield item
