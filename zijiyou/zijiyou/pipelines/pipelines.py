# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.conf import settings
from zijiyou.db.mongoDbApt import MongoDbApt
from zijiyou.items.contentItem import ContentItem
from zijiyou.items.zijiyouItem import ZijiyouItem
import re


class ZijiyouPipeline(object):
    fileApt=None
    mongoApt=None
    
    def __init__(self):
        self.mongoApt=MongoDbApt()
        #self.fileApt = open("zijiyou/pipelines/test.txt","w+")
    
    def process_item(self, item, spider):
        collectionName = ''
        if isinstance(item, ZijiyouItem):
            collectionName = 'daodaoCol'
        elif isinstance(item, ContentItem):
            collectionName = 'responseCol'
            
        # 存到txt文件中
        # self.saveItem2File(item, collectionName)
        self.saveItem2Mongodb(item, collectionName)
        
    def saveItem2File(self,item, collectionName = None):
        values = collectionName + '\n'
        value = ''
        for k,v in item.items():
            try:
                '''if v is not a dic or list will throw exception'''
                value = k+"："+("-".join("%s" % p for p in v))
                value = re.sub("[\r\n]", "", value)+"\n"
            except Exception:
                value = k+"：" + "-" + "%s" % v
            values += value
        self.fileApt.write(values+"\n")
        
    def saveItem2Mongodb(self,item, collectionName):
        values = {}
        value = ''
        for k,v in item.items():
            try:
                '''if v is not a dic or list will throw exception'''
                value = "-".join("%s" % p for p in v)
                value = re.sub("[\r\n]", "", value)+"\n"
            except Exception:
                value = "%s" % v
            values[k] = value
#        print values 
        obj = self.mongoApt.saveItem(collectionName, values)
        print ('++++saveItem2Mongodb++++++++++++++++++++++++++++++++:' ,obj)
