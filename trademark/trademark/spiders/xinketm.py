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



class XinKeSpider(CrawlSpider):
    name = "xinke"
    # start_urls = ['https://www.ht.cn/it-id-1.html']

    start_urls = ["https://www.xinketm.com/Home/Trademark/jiaoyilists.html?classes={}".format(i) for i in range(1,46)]

    rules = (
        Rule(LinkExtractor(allow='&page=\d+',), follow=True),
        Rule(LinkExtractor(allow='jiaoyidetails/\d+.html'), callback='parse_item'),
    )


    def parse_item(self,response):
        item = TrademarkItem()
        # 来源
        source = "鑫科"
        # 来源地址    
        source_url = response.url
        # 申请号
        application = response.xpath('//span[@id="now_tmid"]/@data-tmid').extract()[0]
        # 商标名称
        name = response.xpath('//h3[@class="h3_title"]/text()').extract()[0].replace(" 商标转让","").strip()
        # 类别
        category = response.xpath('//span[@id="now_tmcls"]/@data-tmcls').extract()[0]
        # 出售价
        price = response.xpath('//span[@id="now_tmprice"]/@data-tmprice').extract()[0].replace(',','')
        # 联系人姓名
        contact_name = ""
        # 联系人手机号
        contact_phone = ""
        # 初审公告期号、
        bulletin_issue = ''.join(response.xpath('//div[@class="table-information"]/table[2]//tr/td[2]/text()').extract()).split('第')[-1].replace('期','').replace('暂无数据','').replace('初审公告号','').strip()
        # 初审公告时间、
        bulletin_time = response.xpath('//td[@class="preliminary_issue_date"]/text()').extract()[0].replace('暂无数据','').strip()
        # 源网站对应标的图样
        image = response.xpath('//img[@id="now_tmimg"]/@src').extract()[0]
        if "http" not in image:
            image = "https:" + image

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
        # with open('xinke_goods.json','a') as f:
        #     f.write(json.dumps(item,ensure_ascii=False) + '\n')


        yield item
