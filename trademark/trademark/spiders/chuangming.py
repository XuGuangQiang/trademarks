# coding:utf-8
import scrapy
import logging
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from trademark.items import TrademarkItem
import random
import json
import re
import requests
from lxml import etree
import sys
import requests
import time

reload(sys)
sys.setdefaultencoding('utf-8')

from tools import producer,get_ua

class ChuangMingSpider(CrawlSpider):
    name = "chuangming"

    def start_requests(self):
        yield scrapy.Request("http://www.cmsbw.cn/", callback=self.post_login,dont_filter=True)

    def post_login(self, response):
        url = "http://www.cmsbw.cn/index.php?controller=simple&action=login_act"
        user = "xgq"
        pwd = "xgq17611222661"
        data = {
            "username": user,
            "password": pwd,
            "r": str(random.random())
        }
        yield scrapy.FormRequest(
            url=url,
            formdata=data,
            callback=self.parse_item,
            dont_filter=True
        )

    def parse_item(self, response):
        for i in range(1,46):
            self.get_url(i)
        producer.close()
    def get_url(self,i):
        headers = get_ua()
        for page in range(1,10000000):
            url = "http://www.cmsbw.cn/index.php?controller=site&action=brand_data&page={}&order=b.id+desc&cid={}&boutique=0&r={}".format(page,i,random.random())
            # scrapy.Request(url,callback=self.parse_it,dont_filter=True)
            try:
                response = requests.get(url,headers=headers)
            except:
                try:
                    response = requests.get(url,headers=headers)
                except:
                    continue
            try:
                data = re.findall('"data":.*]',response.content)[0]
            except Exception as e:
                return
            items = json.loads(data.replace('"data":', ''))
            self.parse_text(items)
            time.sleep(1)

    def parse_text(self,items):
        for it in items:
            # item = TrademarkItem()
            item = {}
            try:
                # 来源
                source = "创名"
                # 来源地址
                source_url = "http://www.cmsbw.cn/info-{}.html".format(it['id'])
                # 申请号
                application = ""
                # 商标名称
                name = it['name']
                # 类别
                category = it['num']
                # 出售价
                price = it['price']
                # 联系人姓名
                contact_name = ""
                # 联系人手机号
                contact_phone = ""
                # 初审公告期号、
                bulletin_issue = ""
                # 初审公告时间、
                bulletin_time = ""
                # 源网站对应标的图样
                image = it['img']
                if 'http' not in image:
                    image = "http://www.cmsbw.cn/" + image

                # item = {}
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
                producer.send('tm_web_name', item)
            except:
                pass
