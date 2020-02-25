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



class ZhiGuaGuaSpider(CrawlSpider):
    name = "zhiguagua"

    def start_requests(self):
            yield scrapy.Request("http://market.zgg.com/market/productlist.html", callback = self.parse_item) 


    def parse_item(self,response):
        page_num = response.xpath('//div[@class="tm-product-top"]/div[2]').extract()[-1]
        count_num = re.findall(r'\d+',page_num)[0]
        for i in range(1,(int(count_num)/20)+2):
            url = "http://market.zgg.com/market/productlist.html?p={}".format(i)
            yield scrapy.Request(url=url,callback=self.parse_page1)

    def parse_page1(self,response):
        urls = response.xpath('//ul[@class="tm-mark-pro-list tm-mark-comm-list"]/li/a/@href').extract()
        for u in urls:
            url = "http://market.zgg.com/" + u
            yield scrapy.Request(url=url,callback=self.parse_page)

    def parse_page(self,response):

        # 来源
        source = "知呱呱"
        # 来源地址    
        source_url = response.url
        # 申请号
        application = ""
        # 商标名称
        try:
            name = response.xpath('//div[@class="title"]/h2/text()').extract()[0].replace(" 商标转让","").strip()
        except:
            name = ""
        # 类别
        category = response.xpath('//td[@class="bcomml parsetype className"]/@data-val').extract()[0].split('-')[0].replace('第','').replace('类','').replace('\t','')
        # 出售价
        price = response.xpath('//em[@id="price_info"]/text()').extract()[0].replace('￥', '')
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = ""
        # 初审公告时间、
        bulletin_time = ""
        image = response.xpath('//table[@class="tm-pic-left"]//tr[1]/td/img/@src').extract()[0]

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
        # with open('zhigua_goods.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')


        yield item
