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



class BaiCHengSpider(CrawlSpider):
    name = "baicheng"
    start_urls = ['http://www.100cheng.net/product/index/cate_type/2/id/1/hangye/1.html']

    rules = (
        Rule(LinkExtractor(allow='hangye/\d+.html',),follow=True),
        Rule(LinkExtractor(allow='/p/\d+.html',), follow=True),
        Rule(LinkExtractor(allow='/product/show/id/\d+/cate_type/'), callback='parse_item'),
    )

    def parse_item(self,response):
        # 来源
        source = "百诚商标"
        # 来源地址    
        source_url = response.url
        # 申请号
        application = response.xpath('//div[@class="ng-inxdos-input ng-fault"]/table//tr[1]/td[2]/text()').extract()[0]
        # 商标名称
        name = response.xpath('//div[@class="ng-zexinx-the-tit"]/text()').extract()[0].replace(" 商标转让","").strip()
        # 类别
        category = response.xpath('//div[@class="ng-inxdos-input ng-fault"]/table//tr[1]/td[4]/text()').extract()[0].split('-')[0].replace('第','').replace('类','').replace('\t','')
        # 出售价
        price = ""
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = ""
        # 初审公告时间、
        bulletin_time = response.xpath('//div[@class="ng-inxdos-input ng-fault"]/table//tr[2]/td[2]/text()').extract()[0].replace('无','').strip()
        # 源网站对应标的图样
        image = response.xpath('//div[@class="detailtlbox"]/img/@src | //div[@class="ng-zexthe-show-ims"]/img/@src').extract()[0]
        if "http" not in image:
            image = "http://www.100cheng.net" + image

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
        # with open('baicheng_goods.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')


        yield item