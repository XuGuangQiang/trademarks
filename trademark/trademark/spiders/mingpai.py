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


class MingPaiSpider(CrawlSpider):
    name = "mingpai"
    start_urls = ['http://www.mp.cn/list.html?lb=0&=&page=1']

    rules = (
        Rule(LinkExtractor(allow='&page=\d+',), follow=True),
        Rule(LinkExtractor(allow='id=\d+'), callback='parse_page'),
    )

    
    def start_requests(self):
        yield scrapy.Request("http://www.mp.cn/login.html", callback = self.post_login)  

    def post_login(self,response):
        data = {}
        data['__VIEWSTATE'] = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0]
        data['__EVENTVALIDATION'] = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0]
        data["TxtEmail"] = "13269303178"
        data["TxtRegPassword"]= "1234qwer"
        data["Button1"]= "登录"

        yield FormRequest.from_response(
            response,
            formdata=data,
            callback=self.parse_item
        )
    def parse_item(self,response):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse_page(self,response):
        # 来源
        source = "名派"
        # 来源地址
        source_url = response.url
        # 申请号
        try:
            application = response.xpath('//*[@id="form1"]/div[10]/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[2]/text() | //div[@class="mmp162"]/table//tr[2]/td[2]/text()').extract()[0]  # 注册号
        except Exception as e:
            application = ""
        # 商标名称
        name = response.xpath('//div[@class="rt2"]/text()').extract()[0].split("（")[0]
        # 类别
        category = response.xpath('//*[@id="form1"]/div[10]/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/text() | //div[@class="mmp162"]/table//tr[4]/td[2]/text()').extract()[0].replace('类','').strip()

        # 出售价格
        price = response.xpath('//div[@class="pfprice"]/div/text()').extract()[0]
        if '万' in price:
            price = float(price.replace('万','').replace('会员价：','').strip()) * 10000
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = ""
        # 初审公告时间、
        bulletin_time = ""
        # 商标图片
        image ='http://www.mp.cn' + response.xpath('//div[@class="picc"]/img/@src').extract()[0]

        item = {}
        item['source'] = source
        item['source_url'] = source_url
        item['application'] = application
        item['name'] = name
        item['category'] = str(int(category))
        item['price'] = str(price)
        item['contact_name'] = contact_name
        item['contact_phone'] = contact_phone
        item['bulletin_issue'] = bulletin_issue
        item['bulletin_time'] = bulletin_time
        item['image'] = image
        # with open('mingpai_goods.json', 'a') as f:
        #     f.write(json.dumps(item, ensure_ascii=False) + '\n')
        yield item
