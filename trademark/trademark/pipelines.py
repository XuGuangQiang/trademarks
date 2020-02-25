# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# from kafka import KafkaProducer, KafkaConsumer
# producer = KafkaProducer(value_serializer=lambda v: json.dumps(v,ensure_ascii=False).encode('utf-8'),bootstrap_servers=['115.182.99.138:9092','115.182.99.138:19092','115.182.99.138:19093'])

from spiders.tools import producer

class TrademarkPipeline(object):
    def process_item(self, item, spider):

        producer.send('tm_web_name', item)
