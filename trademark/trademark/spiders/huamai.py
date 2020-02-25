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


class HuaMaiSpider(CrawlSpider):
    name = "huamai"
    start_urls = ["http://www.huamai8.com/Home/Goods/index/p/1.html"]

    rules = (
        Rule(LinkExtractor(allow='/p/\d+.html',), follow=True),
        Rule(LinkExtractor(allow='/id/\d+'), callback='parse_item'),
    )


    def parse_item(self,response):
        # 来源
        source = "华麦"
        # 来源地址
        source_url = response.url
        # 申请号
        application = ""
        # 商标名称
        name = response.xpath('//div[@class="info_r"]/h1//text()').extract()[0].replace(" 商标转让","").strip().split('+')[0]
        # 类别
        category = int(response.xpath('//div[@class="info_r"]/p[2]/text()').extract()[0].split('：')[1].split('-')[0].replace('第','').replace('类',''))
        # 出售价格
        price = response.xpath('//div[@class="price"]/text()').extract()[0].replace('￥','').replace('元','').replace('登录查价','')
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        try:
            contact_phone = response.xpath('//div[@class="contact"]/span[1]/text()').extract()[0]
        except:
            contact_phone = ""
        # 初审公告期号、
        bulletin_issue = ""

        # 初审公告时间、
        bulletin_time = ""
        # 源网站对应标的图样
        image = response.xpath('//div[@class="img"]/img/@src').extract()[0]
        if "http" not in image:
            image = "http://www.huamai8.com/" + image

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
        # with open('huamai.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')

        yield item
