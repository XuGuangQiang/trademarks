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



class MiMaSpider(CrawlSpider):
    name = "mima"

    start_urls = ['http://www.mimatm.com/home/zr/index.html?p=1']

    rules = (
        Rule(LinkExtractor(allow='p=\d+',), follow=True),
        Rule(LinkExtractor(allow='show.html?id=\d+'), callback='parse_item'),
    )


    def parse_item(self,response):
        source = "米马"
        # 来源地址
        source_url = response.url
        # 申请号
        application = response.xpath('//div[@class="R"]/dl[2]/dd/text()').extract()[0]
        # 商标名称
        name = response.xpath('//div[@class="R"]/h1/text()')[0].split('-').extract()[-1]
        # 类别
        category = response.xpath('//div[@class="R"]/h1/text()')[0].split('-').extract()[0].replace('类','')
        # 出售价格
        price = response.xpath('/html/body/div[1]/div[2]/div[3]/dl[3]/dd/i/text()').extract()[0].split('￥')[-1].replace('元','')
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = response.xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[1]/text()').extract()[0].split('：')[-1]
        # 初审公告时间、
        bulletin_time = response.xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[3]/text()').extract()[0].split('：')[-1]
        # 商标图片
        image = 'http://www.mimatm.com' + response.xpath('//div[@class="imgbox"]/img/@src').extract()[0]
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
        # with open('mima_goods.json', 'a') as f:
        #     f.write(json.dumps(item, ensure_ascii=False) + '\n')


        yield item
