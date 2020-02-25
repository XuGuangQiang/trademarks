
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrademarkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 来源
    source = scrapy.Field()
    # 来源地址    
    source_url = scrapy.Field()
    # 申请号
    application = scrapy.Field()
    # 商标名称
    name = scrapy.Field()
    # 类别
    category = scrapy.Field()
    # 出售价格
    price = scrapy.Field()
    # 联系人姓名
    contact_name = scrapy.Field()
    # 联系人手机号
    contact_phone = scrapy.Field()
    # 初审公告期号、
    bulletin_issue = scrapy.Field()
    # 初审公告时间、
    bulletin_time = scrapy.Field()
    # 源网站对应标的图样
    image = scrapy.Field()