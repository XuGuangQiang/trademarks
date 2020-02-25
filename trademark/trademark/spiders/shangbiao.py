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



class ShangBiaoSpider(CrawlSpider):
    name = "shangbiao"

    def start_requests(self):
        yield scrapy.Request("http://www.shsbvip.com/products/list", callback = self.parse_item)


    def parse_item(self,response):
        page_num = response.xpath('//div[@class="pges"]/p/text()').extract()[0]
        count_num = re.findall(r'\d+',page_num)[0]
        for i in range(1,(int(count_num)/30) + 2):
            url = "http://www.shsbvip.com/products/list?is_index=1&between=&bigclassid=0&cg={}#listfirst".format(i)
            yield scrapy.Request(url=url,callback=self.parse_page1)

    def parse_page1(self,response):
        urls = response.xpath('//dd[@class="title"]/a/@href').extract()
        for u in urls:
            url = "http://www.shsbvip.com" + u
            yield scrapy.Request(url=url,callback=self.parse_page)

    def parse_page(self,response):
        # 来源
        source = "尚标"
        # 来源地址
        source_url = response.url
        # 申请号
        application = ""
        # 商标名称
        name = response.xpath('//h1/text()').extract()[0].replace("商标转让","").strip()
        # 类别
        category = re.findall('\d+',response.xpath('//title/text()').extract()[0])[0]
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
        image = response.xpath('//div[@class="disImg"]/img/@src').extract()[0]

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
        # with open('shangbiao.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')


        yield item
