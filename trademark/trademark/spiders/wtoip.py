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



class WtoSpider(CrawlSpider):
    name = "wtoip"

    def start_requests(self):
            yield scrapy.Request("https://ipcc.wtoip.com/buy?pageNo=1&pageSize=40&dictType=100203", callback = self.parse_item) 


    def parse_item(self,response):
        page_num = response.xpath('//div[@class="pages f-fl"]/p/span[1]/text()').extract()[0]
        count_num = re.findall(r'\d+',page_num)[0]
        for i in range(1,int(count_num)+1):
            url = "https://ipcc.wtoip.com/buy?pageNo={}&pageSize=40&dictType=100203".format(i)
            yield scrapy.Request(url=url,callback=self.parse_page1)

    def parse_page1(self,response):
        urls = response.xpath('//ul[@id="icon"]/li/a/@href').extract()
        for u in urls:
            url = "https://ipcc.wtoip.com" + u
            yield scrapy.Request(url=url,callback=self.parse_page)

    def parse_page(self,response):
        item = TrademarkItem()
        # 来源
        source = "汇桔网"
        # 来源地址    
        source_url = response.url
        # 申请号
        application = response.xpath('//div[@class="detailTitle"]//p[@class="title"]/text()').extract()[0].split(' : ')[-1].strip()
        # 商标名称
        name = ''.join(response.xpath('//div[@class="detailTitle"]/h2/text()').extract()).replace(" 商标转让","").strip()
        # 类别
        category = response.xpath('//div[@class="detailTitle"]//p[@class="title"]/text()').extract()[0].split('-')[0].split(' : ')[1].replace('第','').replace('类','').replace('\t','')
        # 出售价
        try:
            price = response.xpath('//span[@class="price"]/text()').extract()[0]
        except:
            price = "面议"
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = ""
        # 初审公告时间、
        bulletin_time = ""
        # 源网站对应标的图样
        image = response.xpath('//ul[@id="shop_img_ul"]//img/@src').extract()[0]

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
        # with open('witoip_goods.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')

        yield item
