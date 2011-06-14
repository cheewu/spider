# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import log
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http.request import Request
from zijiyou.db.mongoDbApt import MongoDbApt
from zijiyou.items.zijiyouItem import Image
import re



class ZijiyouPipeline(object):
    fileApt=None
    mongoApt=None
    specialDb = ["ImageDb"]
    
    def __init__(self):
        if not self.mongoApt:
            self.mongoApt=MongoDbApt()
        #self.fileApt = open("zijiyou/pipelines/test.txt","w+")
    
    def process_item(self, item, spider):
        print "pipeline start"
        print item.collectionName
        if not item.collectionName:
            log.msg("Item的collectionName空！请检查zijiyouItem中是否有未定义collectionName的Item！", level=log.ERROR)
        elif not item.collectionName in self.specialDb:
            # 存到txt文件中
            # self.saveItem2File(item, collectionName)
            self.saveItem2Mongodb(item, item.collectionName)
        else:
            print "++++++++++++++++++++++++++++++-------------------------------------------"
            return item
        
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
        values = {'status':100,
                  'collectionName':item.collectionName}
        value = ''
        for k,v in item.items():
            try:
                '''if v is not a dic or list, a exception will be thrown'''
                value = "-".join("%s" % p for p in v)
            except Exception:
                value = "%s" % v
            values[k] = value
        obj = self.mongoApt.saveItem(collectionName, values)
        print '++++saveItem2Mongodb++++col:%s,objectId:%s' % (collectionName ,obj)
        log.msg('++++saveItem2Mongodb++++col:%s,objectId:%s+++++++++++' % (collectionName ,obj), level = log.INFO)
        

class ZijiyouImagesPipeline(ImagesPipeline):
    mongoApt=None
    imageDb = "ImageDb"
    mongoApt=MongoDbApt()
    
    def get_media_requests(self, item, info):
        log.msg("经过ImagePipeline，开始产生图片请求", level=log.DEBUG)
        if item and item['imageUrl']:
            for url in item['imageUrl']:
                log.msg("产生一个图片链接请求:", level=log.INFO)
                log.msg(url, level=log.INFO)
                yield Request(url)

    def item_completed(self, results, item, info):
        log.msg("图片下载完成", level=log.INFO)
        for ok, x in results:
            if ok and x['path']:
                imageItem = {}
                imageItem['imagePath'] = x['path']
                imageItem['imageUrl'] = x['url']
                log.msg(imageItem, level=log.DEBUG)
                print imageItem
                obj = self.mongoApt.saveItem(self.imageDb, imageItem)
                log.msg('++++saveItem2Mongodb++++col:%s,objectId:%s+++++++++++' % (self.imageDb ,obj), level = log.INFO)
            else:
                raise DropItem("Item contains no images")
        return None        