# coding:utf-8
'''
Created on 2011-8-5

@author: shiym
'''
from pymongo.objectid import ObjectId
from scrapy.conf import settings
from zijiyou.db.apt import mongoApt
import datetime

class DownloaderApt(object):
    '''
    下载器中间件的db适配器
    '''
    
    def __init__(self):
        '''
        初始化
        '''
        self.urlDbnamekey=settings.get('DB_URL')
        self.urlCollectionsMap=settings.get('DB_URL_COLLECTIONS_MAP')
    
    def updateUrlDbStatusById(self,urlId,spiderName,status=200):
        '''
        更新数据库访问状态
        '''
        whereJson={"_id":ObjectId(urlId)}
        updateJson={"status":status, "dateTime":datetime.datetime.now()}
        mongoApt.update(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson, updateJson=updateJson)
    
    def updateUrlDbStatusByUrl(self,url,spiderName,status=200):
        '''
        更新数据库访问状态
        '''
        whereJson={"url":url}
        updateJson={"status":status, "dateTime":datetime.datetime.now()}
        mongoApt.update(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson, updateJson=updateJson)
    
    def getRandonValidProxy(self):
        '''
        从数据库选择一个随机的有效代理
        '''
        raise NotImplemented('从数据库选择一个随机的有效代理还没有实现')
