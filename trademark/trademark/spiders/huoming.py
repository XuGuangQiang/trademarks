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



class HuoMingSpider(CrawlSpider):
    name = "huoming"

    def start_requests(self):
            yield scrapy.Request("https://www.huoming.com/tradeMark_0_0_0_0_0_createDate_DESC_1.html", callback = self.parse_item) 


    def parse_item(self,response):
        page_num = response.xpath('//div[@id="pagination"]/@data-total').extract()[0]
        count_num = re.findall(r'\d+',page_num)[0]
        for i in range(1,(int(count_num)/50)+2):
            url = "https://www.huoming.com/tradeMark_0_0_0_0_0_createDate_DESC_{}.html".format(i)
            yield scrapy.Request(url=url,callback=self.parse_page1)

    def parse_page1(self,response):
        urls = response.xpath('//ul[@class="trade-list clearfix"]/li/a[1]/@href').extract()
        for u in urls:
            yield scrapy.Request(url=u,callback=self.parse_page)

    def parse_page(self,response):

        # 来源
        source = "火名网"
        # 来源地址    
        source_url = response.url
        # 申请号
        application = response.xpath('//table[@class="table"]//tr[2]/td[4]/text()').extract()[0]
        # 商标名称
        name = response.xpath('//table[@class="table"]//tr[2]/td[2]/text()').extract()[0].replace(" 商标转让","").strip()
        # 类别
        category = response.xpath('//table[@class="table"]//tr[3]/td[2]/text()').extract()[0].split('-')[0].replace('第','').replace('类','').replace('\t','')
        # 出售价
        try:
            price = response.xpath('//div[@class="price"]/span/i/text()').extract()[0].repalce(',','')
        except:
            price = ""
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        try:
            bulletin_issue = response.xpath('//table[@class="table"]//tr[4]/td[2]/text()').extract()[0]
        except:
            bulletin_issue = ""
        # 初审公告时间、
        try:
            bulletin_time = response.xpath('//table[@class="table"]//tr[5]/td[2]/text()').extract()[0].strip()
        except:
            bulletin_time = ""
        # 源网站对应标的图样
        image = response.xpath('//table[@class="table"]//tr[1]/td[2]/img/@src').extract()[0]

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
    
        # with open('huoming_goods.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')



        yield item
