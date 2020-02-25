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
sess.get("https://www.zhiguoguo.com/")

class ZhiGuoGuoSpider(CrawlSpider):
    name = "zhiguoguo"

    def start_requests(self):
        yield scrapy.Request("https://www.zhiguoguo.com/", callback=self.parse_item)

    def parse_item(self, response):
        self.login()
        for i in range(1,46):
            if i < 10:
                i = "0" + str(i)
            self.parse_item1(i)
        producer.close()

    def login(self):
        url = "https://www.zhiguoguo.com/user/login"
        user = "17611222661"
        pwd = "xgq17611222661"
        data = {
            "passport": user,
            "passwd": pwd
        }
        sess.post(url, data=data, timeout=10)

    def parse_item1(self,i):

        page = 1
        url = "https://www.zhiguoguo.com/category/findTwsTrademarkDealInfo"
        while 1:
            headers = get_ua()
            headers['Content-Type'] = 'application/json'
            data = {"pageParam": {"pageNo": str(page), "pageSize": "10"},"pcCall": "1","searchType": "1","keyWord": "","type": "","category":i}
            try:
                req = sess.post(url,data=json.dumps(data),headers=headers,timeout=4)
            except:
                try:
                    req = sess.post(url, data=json.dumps(data), headers=headers, timeout=4)
                except:
                    pass
            try:
                goods_datas = json.loads(req.content)['data']['list']
            except:
                continue
            if not goods_datas:
                break
            self.parse_page(goods_datas,i)
            page += 1
            time.sleep(0.5)
    def parse_page(self, datas,goods_type):
        for data in datas:
            try:
                # 来源
                source = "知果果"
                # 来源地址
                source_url = "https://www.zhiguoguo.com/trade/trademarkDetail/3/" + data['appcode']
                # 申请号
                application = data['appcode']
                # 商标名称
                try:
                    name = data['trname']
                except:
                    name = ""
                # 类别
                category = str(int(goods_type))
                # 出售价格
                price = data['lastSellPrice']
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
                    image = data['trUrl']
                except:
                    image = ""
            except Exception as e:
                continue

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
            # with open('zhiguo_goods.json','a') as f:
            #     f.write(json.dumps(item,ensure_ascii=False) + '\n')