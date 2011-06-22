# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from zijiyou.db.mongoDbApt import MongoDbApt
import datetime

class ErrorFlag(object):
    ACCESS_DENY_FLAG = 0
    
class UpdateRequestedUrl(object):
    '''
    访问过的url更新数据库
    '''
    def __init__(self):
        self.mongoApt=MongoDbApt()
        self.CrawlDb=settings.get('CRAWL_DB')
        self.ResponseDb=settings.get('RESPONSE_DB')
        if not self.CrawlDb or not self.ResponseDb:
            log.msg('没有配置CRAWL_DB！，请检查settings', level=log.ERROR)
            raise NotConfigured
    
    def process_response(self, request, response, spider):
        whereJson={"url":request.url}
        responseStatus=response.status
        updateJson={"status":200, "dateTime":datetime.datetime.now()}
        if responseStatus:
            updateJson["status"]=responseStatus
        if responseStatus in [400, 403]:
            log.msg("%s 错误！爬取站点可能拒绝访问或拒绝响应" % responseStatus, level=log.ERROR)
        self.mongoApt.updateItem(self.CrawlDb,whereJson,updateJson)
        log.msg("downloader中间件更新数据库访问状态。 url:%s" % request.url, level=log.INFO)
        return response

class RandomHttpProxy(object):
    proxyNum  = -1
    curProxyIndex = -1 # use local network, not set proxy
    proxies = []
    
    def process_request(self, request, spider):
        '''init proxy configure'''
        if(self.proxyNum == -1 and settings['PROXY'] != None):
            self.proxies = settings['PROXY']
            self.proxyNum = len(self.proxies)
        
        if(self.proxyNum > 0):
            #next proxy
            self.curProxyIndex = (self.curProxyIndex + 1) % self.proxyNum
            #ignore the next proxy is local
            if(self.proxies[self.curProxyIndex] != 'local'):
                #set proxy
                request.meta['proxy'] = '%s' % self.proxies[self.curProxyIndex]
                log.msg('change proxy:'+self.proxies[self.curProxyIndex], level = log.INFO)
            else:
                log.msg('change proxy:use local network', level = log.INFO)
        return None