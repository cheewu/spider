# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from scrapy import log
from scrapy.conf import settings

class ErrorFlag(object):
    ACCESS_DENY_FLAG = 0

from zijiyou.db.mongoDbApt import MongoDbApt

class RequestedUrlUpdate(object):
    '''
    访问过的url更新数据库
    '''
    mongoApt=None
    colName="crawlCol"
    def __init__(self):
        if not self.mongoApt:
            self.mongoApt=MongoDbApt()
    
    def process_response(self, request, response, spider):
#        log.msg("开始调用downloadmid中间件",level=log.INFO)
        whereJson={"url":request.url}
        responseStatus=response.status
        updateJson={"status":1}
        if responseStatus:
            updateJson["status"]=responseStatus
        if responseStatus in [400, 403]:
            log.msg("%s 错误！爬取站点可能拒绝访问或拒绝响应" % responseStatus, level=log.ERROR)
            if request.meta:
                meta=request.meta
                meta["status"]=responseStatus
#                request.replace(meta)
        self.mongoApt.updateItem(self.colName,whereJson,updateJson)
        log.msg("recentRequests 更新数据库访问状态。 url:%s" % request.url, level=log.INFO)
#        log.msg("成功调用downloadmid中间件",level=log.INFO)
        return response

class RandomHttpProxy(object):
    proxyNum  = -1
    curProxyIndex = -1 # use local network, not set proxy
    proxies = []
    
    def process_request(self, request, spider):
        '''init proxy configure'''
        if(self.proxyNum == -1 and settings['PROXY'] != None):
            self.proxyNum = len(self.proxies)
            #print self.proxies
        
        ErrorFlag.ACCESS_DENY_FLAG = 1
        if(self.proxyNum > 0):
            if(ErrorFlag.ACCESS_DENY_FLAG == 1):
                #next proxy
                self.curProxyIndex = (self.curProxyIndex + 1) % self.proxyNum
                #ignore the next proxy is local
                if(self.proxies[self.curProxyIndex] != 'local'):
                    #set proxy
                    request.meta['proxy'] = '%s' % self.proxies[self.curProxyIndex]
                    print 'change proxy:', self.proxies[self.curProxyIndex]
                    log.msg('change proxy:'+self.proxies[self.curProxyIndex], level = log.INFO)
                else:
                    print 'change proxy: local network'
                    log.msg('change proxy:use local network', level = log.INFO)
                    
                #set the access_error to 0
                ErrorFlag.ACCESS_DENY_FLAG = 0
            else:
                # use local network, not set proxy
                if(self.curProxyIndex < 0):
                    print 'use current proxy: local network'
                    log.msg('use current proxy: local network', level = log.INFO)
                else:
                    #set the current proxy
                    request.meta['proxy'] = '%s' % self.proxies[self.curProxyIndex]
                    print 'use current proxy:', self.proxies[self.curProxyIndex]
                    log.msg('use current proxy:'+self.proxies[self.curProxyIndex], level = log.INFO)
                
            
class ResponseStatusCheck(object):
    
    def process_response(self, request, response, spider):
        print 'check response status'
        '''check the response status '''
        ''' status: 403, denied to access, solution: change the http proxy by set a flag to ACCESS_DENY_FLAG = 1 , then the RandomHttpProxy will change the proxy by the flag'''
        if(response.status in [400, 403]):
            log.msg('set access_deny flag-response status %s' %  response.status, level = log.INFO)
            ErrorFlag.ACCESS_DENY_FLAG = 1
        return response
