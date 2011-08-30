# coding:utf-8
'''
Created on 2011-8-5

@author: shiym
'''
from pymongo.objectid import ObjectId
from zijiyou.db.apt import mongoApt
import datetime

class DownloaderApt(object):
    '''
    下载器中间件的db适配器
    '''
    
    def updateUrlDbStatusById(self,urlId,status=200):
        '''
        更新数据库访问状态
        '''
        colName='UrlDb'
        whereJson={"_id":ObjectId(urlId)}
        updateJson={"status":status, "dateTime":datetime.datetime.now()}
        mongoApt.update(colName, whereJson=whereJson, updateJson=updateJson)
    
    def updateUrlDbStatusByUrl(self,url,status=200):
        '''
        更新数据库访问状态
        '''
        colName='UrlDb'
        whereJson={"url":url}
        updateJson={"status":status, "dateTime":datetime.datetime.now()}
        mongoApt.update(colName, whereJson=whereJson, updateJson=updateJson)
    
    def getRandonValidProxy(self):
        '''
        从数据库选择一个随机的有效代理
        '''
        raise NotImplemented('从数据库选择一个随机的有效代理还没有实现')
                
#class SchedulerApt(object):
#    '''
#    调度器中间件的db适配器
#    '''
#    
    
    
    
        