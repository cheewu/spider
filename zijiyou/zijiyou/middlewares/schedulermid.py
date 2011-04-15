# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from scrapy import log
from scrapy.conf import settings
from zijiyou.db.mongoDbApt import MongoDbApt
import datetime



class RequestSaver(object):
    '''
    新调度保存入数据库
    '''
    mongoApt=None
    colName="crawlCol"
    def __init__(self):
        if not self.mongoApt:
            self.mongoApt=MongoDbApt()

    def enqueue_request(self,spider,request):
#        log.msg("开始调用schedulermid中间件",level=log.INFO)
        recentReq={"url":"","callBack":None,"status":"","priority":1,"dateTime":datetime.datetime.now()}
        recentReq["url"]=request.url
        meta=request.meta
        if meta and "callBack" in meta:
            recentReq["callBack"]=request.meta["callBack"]
        recentReq["priority"]=request.priority
        recentReq["status"]=1000
        
        queJson={"url":request.url}
        if not self.mongoApt.isExist(self.colName, queJson):
            self.mongoApt.saveItem(self.colName,recentReq)
            log.msg("保存新request：%s" % request.url,level=log.INFO)
        else:
            log.msg("重复的request，不执行保存：%s" % request.url,level=log.INFO)
        
        spider.recentRequests.append(recentReq)
        maxRecentUrlsSize=settings.get('RECENT_URLS_SIZE',300)
        while len(spider.recentRequests) > maxRecentUrlsSize:
            spider.recentRequests.pop(0)
#        log.msg("成功完成调用schedulermid中间件",level=log.INFO)
        return None
    
    