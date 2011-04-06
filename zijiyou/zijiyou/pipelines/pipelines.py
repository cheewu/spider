# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import re

from zijiyou.pipelines.mongoDbApt import MongoDbApt

class ZijiyouPipeline(object):
    fileApt=None
    mongoApt=None
    
    def __init__(self):
        self.mongoApt=MongoDbApt()
        #self.fileApt = open("zijiyou/pipelines/test.txt","w+")
    
    def process_item(self, item, spider):
        # 存到txt文件中
        # self.saveItem2File(item)
        self.saveItem2Mongodb(item)
        
    def saveItem2File(self,item):
        values="\n"        
        for k,v in item.items():
            value=k+"："+("-".join("%s" % p for p in v))
            values+=re.sub("[\r\n]", "", value)+"\n"
        self.fileApt.write(values+"\n")
        
    def saveItem2Mongodb(self,item):
        values={}
        for k,v in item.items():
            values[k]=v
        print values 
        obj = self.mongoApt.saveItem("daodaoCol", values)
        print ('++++saveItem2Mongodb++++++++++++++++++++++++++++++++:' ,obj)
        
        
        
        