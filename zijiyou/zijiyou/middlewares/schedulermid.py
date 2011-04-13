# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from scrapy.conf import settings
from scrapy import log

from zijiyou.db.mongoDbApt import MongoDbApt

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
        log.msg("开始调用schedulermid中间件",level=log.INFO)
        recentReq={"url":"","callBack":"","status":"","priority":1}
        recentReq["url"]=request.url
#        recentReq["callBack"]=request.meta["callBack"]
        recentReq["priority"]=request.priority
        recentReq["status"]=0
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print recentReq
        self.mongoApt.saveItem(self.colName,recentReq)
        log.msg("保存新request：%s" % recentReq["url"],level=log.INFO)
        
        spider.recentRequests.append(recentReq)
        maxRecentUrlsSize=settings.get('RECENT_URLS_SIZE',300)
        while len(spider.recentRequests) > maxRecentUrlsSize:
            spider.recentRequests.pop(0)
        log.msg("成功完成调用schedulermid中间件",level=log.INFO)
        return None
    
    