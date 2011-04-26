# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import log
from zijiyou.db.mongoDbApt import MongoDbApt
from zijiyou.items.zijiyouItem import Attraction,ResponseBody,Note,CommonSense
import re


class ZijiyouPipeline(object):
    fileApt=None
    mongoApt=None
    
    def __init__(self):
        if not self.mongoApt:
            self.mongoApt=MongoDbApt()
        #self.fileApt = open("zijiyou/pipelines/test.txt","w+")
    
    def process_item(self, item, spider):
        if item.collectionName:
            # 存到txt文件中
            # self.saveItem2File(item, collectionName)
            self.saveItem2Mongodb(item, item.collectionName)
        
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
            if k != 'status':
                try:
                    '''if v is not a dic or list, a exception will be thrown'''
                    value = "-".join("%s" % p for p in v)
                except Exception:
                    value = "%s" % v
            else:
                if v[0]:
                    value = v[0]
                else:
                    value = 100
            values[k] = value
        obj = self.mongoApt.saveItem(collectionName, values)
        print '++++saveItem2Mongodb++++col:%s,objectId:%s' % (collectionName ,obj)
        log.msg('++++saveItem2Mongodb++++col:%s,objectId:%s+++++++++++' % (collectionName ,obj), level = log.INFO)
