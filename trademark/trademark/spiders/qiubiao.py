# coding:utf-8
import scrapy
import logging
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from trademark.items import TrademarkItem
import time
import json
import re
import requests
from lxml import etree
import sys
from tools import producer,get_ua

reload(sys)
sys.setdefaultencoding('utf-8')
sess = requests.session()
sess.get("https://www.qiutm.com/")

class QiuBiaoSpider(CrawlSpider):
    name = "qiubiao"

    def start_requests(self):
        yield scrapy.Request("https://www.qiutm.com/", callback=self.parse_item)

    def login(self):
        headers = get_ua()
        user = '17611222661'
        pwd = 'xgq17611222661'
        url = "https://www.qiutm.com/customer/login"
        data = {"telephone": user, "password": pwd, "type": ""}
        sess.post(url, data=data)

    def parse_item(self, response):
        for i in range(1,46):
            if i < 10:
                i = "0" + str(i)
            self.parse_item1(i)
        producer.close()

    def parse_item1(self,i):
        self.login()
        page = 1
        while 1:
            headers = get_ua()
            url = "https://www.qiutm.com/trademark/"
            data = {"pageNum": str(page), "pageSize": "40", "firstClsCode": i}
            try:
                req = sess.post(url, headers=headers, data=data)
                datas = req.text
                items = json.loads(datas)
            except:
                req = sess.post(url, headers=headers, data=data)
                datas = req.text
                try:
                    items = json.loads(datas)
                except:
                    continue
            if not items['data']['result']['rows']:
                break
            self.parse_page(items['data']['result']['rows'])
            sess.headers.update({'Referer': url})

    def parse_page(self, goodss):
        for goods in goodss:
            try:
                # 来源
                source = "求标"
                # 来源地址
                source_url = "https://www.qiutm.com/trademark/details/" + str(goods['id'])
                # 申请号
                application = goods['regNo']
                # 商标名称
                try:
                    name = goods['tmName']
                except:
                    name = ""
                category = str(int(goods['firstClsCode']))
                # 出售价格
                try:
                    price = goods['price'].replace('￥', '').strip()
                except:
                    price = ""
                # 联系人姓名
                contact_name = ""
                # 联系人手机号
                contact_phone = ""
                # 初审公告期号、
                bulletin_issue = ""
                # 初审公告时间、
                bulletin_time = ""
                # 源网站对应标的图样
                try:
                    image = goods['imgUrl']
                except:
                    image = ""

                item = {}
                item['source'] = source
                item['source_url'] = source_url
                item['application'] = application
                item['name'] = name
                item['category'] = category
                item['price'] = price
                item['contact_name'] = contact_name
                item['contact_phone'] = contact_phone
                item['bulletin_issue'] = bulletin_issue
                item['bulletin_time'] = bulletin_time
                item['image'] = image
                producer.send('tm_web_name', item)
            except:
                pass