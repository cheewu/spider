# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from scrapy.conf import settings
from scrapy import log

from zijiyou.db.mongoDbApt import MongoDbApt

class RequestedUrlUpdate(object):
    mongoApt=None
    colName="crawlCol"
    def __init__(self):
        if not self.mongoApt:
            self.mongoApt=MongoDbApt()
    
    '''
    访问过的url更新数据库
    '''
    def process_response(self, request, response, spider):
        log.msg("开始调用downloadmid中间件",level=log.INFO)
        whereJson={"url":request.url}
        updateJson={"status":1}
        print '-------------------------------------------------------'
        print whereJson      
        log.msg("recentRequests 更新数据库：", level=log.INFO)
        self.mongoApt.updateItem(self.colName,whereJson,updateJson)  
        log.msg("成功调用downloadmid中间件",level=log.INFO)
        return response

class RandomHttpProxy(object):
    proxyNum  = -1
    curProxyIndex = 0
    proxies = []

    def process_request(self, request, spider):
        '''init proxy configure'''
        if(self.proxyNum == -1):
            self.proxies = settings['PROXY']
            #print self.proxies
            self.proxyNum = len(self.proxies)
            
        if(self.proxyNum != 0):
            request.meta['proxy'] = self.proxies[self.curProxyIndex]
            self.curProxyIndex = (self.curProxyIndex + 1) % self.proxyNum
