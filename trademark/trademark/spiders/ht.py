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
from tools import ht


class HaoTingSpider(CrawlSpider):
    name = "haoting"
    # start_urls = ['https://www.ht.cn/it-id-1.html']
    start_urls = ht()

    rules = (
        Rule(LinkExtractor(allow='it-id-\d+-p-\d+',), follow=True),
        Rule(LinkExtractor(allow='/dt-id-\d+'), callback='parse_page'),
    )

    
    def start_requests(self):
            yield scrapy.Request("https://www.ht.cn/User-index.html", callback = self.post_login)  

    def post_login(self,response):
        user = "xgq_qgx123"
        pwd = "xgq17611222661"
        yield FormRequest.from_response(
            response,
            formdata={"name": user, "password": pwd,"Submit": "登录"},
            callback=self.parse_item
        )
    def parse_item(self,response):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse_page(self,response):
        item = TrademarkItem()
        # 来源
        source = "好听商标"
        # 来源地址    
        source_url = response.url
        # 申请号
        application = ""
        # 商标名称
        name = response.xpath('//h1/text()').extract()[0].replace(" 商标转让","").strip()
        # 类别
        category = response.xpath('//*[@id="tmleftbox1"]/div[2]/ul[1]/div[2]/ul/dl/dd[1]/a/text()').extract()[0].replace('第','').replace('类','')
        # 出售价格
        try:
            price = response.xpath('//*[@id="tmleftbox1"]/div[2]/ul[1]/div[2]/ul/li/font[1]/text()').extract()[0].split(':')[1]
        except:
            try:
                price = response.xpath('//*[@id="tmleftbox1"]/div[2]/ul[1]/div[2]/ul/li/text()').extract()[0]
            except:
                with open('ht.txt','a') as f:
                    f.write(response.url + '\n')
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = response.xpath('//*[@id="tbs"]//tr[4]/td[2]/text()').extract()[0]
        # 初审公告时间、
        bulletin_time = response.xpath('//*[@id="tbs"]//tr[5]/td[2]/text()').extract()[0]
        # 源网站对应标的图样
        image = response.xpath('//ul[@class="info"]/div/img/@src').extract()[0]
        if 'http' not in image:
            image = "https:" + image

        item = {}
        item['source'] = source
        item['source_url'] = source_url
        item['application'] = application
        item['name'] = name
        item['category'] = str(int(category))
        item['price'] = price.replace('参考价:','').replace('价格：￥','').replace('元','').replace('￥','').replace('元','').strip()
        item['contact_name'] = contact_name
        item['contact_phone'] = contact_phone
        item['bulletin_issue'] = bulletin_issue
        item['bulletin_time'] = bulletin_time
        item['image'] = image
        yield item
