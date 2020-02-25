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
from multiprocessing.dummy import Pool as ThreadPool
reload(sys)
sys.setdefaultencoding('utf-8')
sess = requests.session()
sess.get("https://www.maizhi.com")

class MaiZhiSpider(CrawlSpider):
    name = "maizhi"

    def start_requests(self):
        yield scrapy.Request("https://www.maizhi.com", callback=self.parse_item)

    def login(self):
        headers = get_ua()
        token_url = "https://www.maizhi.com/login?ref_url=https%3A%2F%2Fwww.maizhi.com%2F"
        req = sess.get(token_url, headers=headers, timeout=10)
        html = etree.HTML(req.content)
        try:
            token = html.xpath('//input[@name="_token"]/@value')[0]
        except:
            token_url = "https://www.maizhi.com/login?ref_url=https%3A%2F%2Fwww.maizhi.com%2F"
            req = sess.get(token_url, headers=headers, timeout=10)
            html = etree.HTML(req.content)
            token = html.xpath('//input[@name="_token"]/@value')[0]

        user = "xgq"
        pwd = "xgq17611222661"

        data = {
            "_token": token,
            "ref_url": "https://www.maizhi.com/",
            "loginname": user,
            "member_passwd": pwd
        }
        login_url = "https://www.maizhi.com/login"
        sess.post(login_url, headers=headers, data=data)

    def parse_item(self, response):

        class_urls = ["https://www.maizhi.com/search/?category={}&curpage=".format(i) for i in range(1, 46)]
        for url in class_urls:
            self.parse_item1(url)
        producer.close()

    def parse_item1(self,url):
        self.login()
        page = 1
        # pool = ThreadPool(5)
        while 1:
            url_page = url + str(page)
            try:
                req = sess.get(url_page,timeout=10)
            except:
                req = sess.get(url_page,timeout=10)
            txt = req.content
            html = etree.HTML(txt)
            goods_urls = html.xpath('//ul[@class="tm-lists"]/li/a/@href')
            uls = ["https://www.maizhi.com" + u for u in goods_urls]
            if len(goods_urls) <=0:
                return
            else:
                # pool.map(self.parse_page, uls)
                self.parse_page(uls)
                page += 1
        # pool.close()
        # pool.join()

    def parse_page(self, uls):
        for url in uls:
            headers = get_ua()
            try:
                req = sess.get(url, headers=headers, timeout=10)
            except:
                return
            txt = req.content
            html = etree.HTML(txt)
            # 来源
            source = "麦知"
            # 来源地址
            source_url = url
            # 申请号
            application = ""
            # 商标名称
            try:
                name = html.xpath('//span[@class="tm_name"]/text()')[0].replace(" 商标转让", "")
            except:
                return ""
            # 类别
            category = html.xpath('//div[@class="item tm_intcls"]/span/text()')[0].replace('第', '').replace('类', '')
            # 出售价格
            price = html.xpath('//div[@class="price"]/span/text()')[0].split(' ')[1]
            # 联系人姓名
            contact_name = ""
            # 联系人手机号
            contact_phone = ""
            # 初审公告期号、
            bulletin_issue = html.xpath('//table//tr[1]/td[2]/text()')[0]
            # 初审公告时间、
            bulletin_time = html.xpath('//table//tr[2]/td[2]/text()')[0]
            # 源网站对应标的图样
            image = re.findall(r'url\((.*?)\)', html.xpath('//div[@class="img-container"]/@style')[0])[0]

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
            producer.send('tm_web_name', item)
