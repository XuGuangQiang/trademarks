# coding:utf-8
import scrapy
import logging
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from trademark.items import TrademarkItem
import json
import re
import time
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class MingPinSpider(CrawlSpider):
    name = "mingpin"

    start_urls = ['http://www.mp.cc/search/1']

    rules = (
        Rule(LinkExtractor(allow='/search/\d+?',), follow=True),
        Rule(LinkExtractor(allow='/detail/\d+'), callback='parse_item'),
    )


    def parse_item(self,response):
        # 来源
        source = "名品商标"
        # 来源地址
        source_url = response.url
        # 申请号
        try:
            application = response.xpath('//*[@id="body"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/span/text() | //*[@id="body"]/div/div[2]/div[3]/div[1]/div[3]/table/tbody/tr[1]/td[4]/text()').extract()[0]
        except Exception as e:
            application = ""
        # 商标名称
        name = response.xpath('//div[@class="d_top_rt_left"]/text()').extract()[0].replace("商标转让","").strip()
        # 类别
        category = re.findall('\d+',response.xpath('//*[@id="body"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/span/text()').extract()[0])[0]
        # 出售价
        price = ""
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = ""
        # 初审公告时间、
        bulletin_time = response.xpath('//div[@class="intr_item"]/table//tr[2]/td[2]/span/text()').extract()[0].replace('无','').strip()
        # 源网站对应标的图样
        image = response.xpath('//div[@class="d_top_lt_img"]/img/@src').extract()[0]

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
        # with open('mingpin.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')


        yield item
