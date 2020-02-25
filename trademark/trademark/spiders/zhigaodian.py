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
from tools import zgd


class ZhiGaoDianSpider(CrawlSpider):
    name = "zhigaodian"
    start_urls = zgd()

    rules = (
        Rule(LinkExtractor(allow='page\d+',), follow=True),
        Rule(LinkExtractor(allow='/goods/\d+'), callback='parse_item'),
    )
    def start_requests(self):
            yield scrapy.Request("https://www.ipvip.cn/home/ipviplogin.html", meta={'cookiejar':1},callback=self.post_login,dont_filter=True)  

    def post_login(self,response):
        user = "17611222661"
        pwd = "xgq17611222661"
        return scrapy.FormRequest(
            # response,
            url = "https://www.ipvip.cn/home/ipVipLogin.do",
            formdata= {"username": user, "password": pwd},
            meta = {'cookiejar':response.meta['cookiejar']},
            callback=self.parse_page
        )
    def parse_page(self,response):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse_item(self,response):
        # 来源
        source = "智高点"
        # 来源地址    
        source_url = response.url
        # 申请号
        application = response.xpath('//div[@class="regdetail"]//td[3]/text()').extract()[0]
        # 商标名称
        name = response.xpath('//div[@class="regdetail"]//td[1]/text()').extract()[0].replace(" 商标转让","").strip()
        # 类别
        category = response.xpath('//div[@class="regdetail"]//td[2]/text()').extract()[0].split('-')[0].replace('第','').replace('类','').replace('\t','')
        # 出售价
        try:
            price = response.xpath('//b[@id="sellPrice"]/text()').extract()[0]
        except:
            price = "面议"
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = response.xpath('//div[@class="regdetail"]//td[6]/text()').extract()[0]
        # 初审公告时间、
        bulletin_time = response.xpath('//div[@class="regdetail"]//td[5]/text()').extract()[0].replace('无','').strip()
        # 源网站对应标的图样
        image = response.xpath('//*[@id="ban_pic1"]/ul/li[1]/img/@src').extract()[0]
        if "http" not in image:
            image = "https://www.ipvip.cn" + image

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
        # with open('zhigaodian_goods.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')

        yield item
