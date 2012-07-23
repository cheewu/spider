# -*- coding: utf-8 -*-
'''
Created on 2011-6-22

@author: shiym
'''
from scrapy import log
from scrapy.exceptions import NotConfigured
from zijiyou.db.pipelineApt import StorageApt
from zijiyou.common import utilities
import leveldb
import re

class StoragePipeline(object):
#    specialDb = ["ImageDb"]
    
    def __init__(self):
        self.apt=StorageApt()
        self.leveldb=leveldb.Leveldb('./pagecontentdb')
        
    def process_item(self, item, spider):
        if not item['collectionName']:
            log.msg("Item的collectionName空！请检查zijiyouItem中是否有未定义collectionName的Item！", level=log.ERROR)
            raise NotConfigured
        md5Val = utilities.getFingerPrint(item['url'], isUrl=True)
        self.leveldb.Put(md5Val,item['responseBody'])
        self.saveItem2Mongodb(item, item['collectionName'],spider.name)
        
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
        
    
    def saveItem2Mongodb(self,item, collectionName,spiderName):
        values = {}
        for k,v in item.items():
            if k=='responseBody':
                continue
            values[k] = v
        obj=self.apt.saveItem(collectionName, values,spiderName)
        log.msg('++++saveItem2Mongodb++++col:%s,objectId:%s+++++++++++' % (collectionName ,obj), level = log.INFO)
        
    