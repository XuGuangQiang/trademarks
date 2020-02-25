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
from tools import ghip


class GaoHangSpider(CrawlSpider):
    name = "gaohang"
    # start_urls = ['https://www.ht.cn/it-id-1.html']
    start_urls = ghip()
    # start_urls = ['http://r.gaohangip.com/search?scope=1&tc=1']

    rules = (
        Rule(LinkExtractor(allow='&tc=\d+',),follow=True),
        Rule(LinkExtractor(allow='&pagenumber=\d+',), follow=True),
        Rule(LinkExtractor(allow='trademark/\d+.html'), callback='parse_item'),
    )


    def parse_item(self,response):
        # 来源
        source = "高航商标"
        # 来源地址    
        source_url = response.url
        # 申请号
        application = response.xpath('//div[@class="item_registerNO fl"]/span/@title').extract()[0]
        # 商标名称
        name = response.xpath('//h1/@title').extract()[0].replace(" 商标转让","").strip()
        # 类别
        category = int(response.xpath('//div[@class="item_sbType fl"]/span/@title').extract()[0].replace('第','').split('-')[0].replace('类',''))
        # 出售价格
        price = response.xpath('//span[@class="sell_priceW"]/text()').extract()[0].replace(',','')
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        try:
            bulletin_issue = response.xpath('//div[@class="sb_detail_con"]/ul/li[1]/p[2]/text()').extract()[0].replace('无\r\n','').strip()
        except:
            bulletin_issue = ""
        # 初审公告时间、
        try:
            bulletin_time = response.xpath('//div[@class="sb_detail_con"]/ul/li[2]/p[2]/text()').extract()[0].replace('无\r\n','').strip()
        except:
            bulletin_time = ""
        # 源网站对应标的图样
        image = response.xpath('//img[@id="ShowPic"]/@src').extract()[0]

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
        # with open('gh_goods.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')

        yield item
