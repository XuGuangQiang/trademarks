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


class BiaoTianXiaSpider(CrawlSpider):
    name = "biaotianxia"

    start_urls = ['https://biaotianxia.com/display_producm.php?&page=1']

    rules = (
        Rule(LinkExtractor(allow='&page=\d+',), follow=True),
        Rule(LinkExtractor(allow='_\d+.html'), callback='parse_item')
    )


    def parse_item(self,response):
        # 来源
        source = "标天下"
        # 来源地址
        source_url = response.url
        # 申请号
        try:
            application = response.xpath('//div[@class="fake"]/p/span[1]/text()').extract()[0]
        except:
            application = ""
        # 商标名称
        name = response.xpath('//div[@class="title_s"]/strong/text()').extract()[0].replace("商标转让","").strip()
        # 类别
        category = re.findall('\d+',response.xpath('//div[@class="titles cl"]/a[2]/text()').extract()[0])[0]
        # 出售价
        price = ""
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = response.xpath('//*[@id="header"]/table//tr[1]/td[2]/table//tr[2]/td/table//tr/td[2]/text()').extract()[0].replace('初审公告期号：','')
        # 初审公告时间、
        bulletin_time = ""
        # 源网站对应标的图样
        image = response.xpath('//div[@class="ins_a"]/img/@src').extract()[0]
        if "http" not in image:
            image = "https://biaotianxia.com/" + image

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
        # with open('biaotianxia.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')


        yield item
