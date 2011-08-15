# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from scrapy.http.response import Response
from zijiyou.db.middlewaresApt import DownloaderApt

class ErrorFlag(object):
    ACCESS_DENY_FLAG = 0
    
class UpdateRequestedUrl(object):
    '''
    访问过的url更新数据库
    '''
    def __init__(self):
        self.apt=DownloaderApt()
        self.CrawlDb=settings.get('CRAWL_DB')
        self.ResponseDb=settings.get('RESPONSE_DB')
        if not self.CrawlDb or not self.ResponseDb:
            log.msg('没有配置CRAWL_DB！，请检查settings', level=log.ERROR)
            raise NotConfigured
    
#    def process_request(self,request, spider):
#        print 'downMid reqOut test get:%s' % request.url 
    
    def process_response(self, request, response, spider):
#        if not isinstance(response,Response):
#            return response
        responseStatus=response.status
        if responseStatus in [400, 403, 304]:
            log.msg("%s 错误！爬取站点可能拒绝访问或拒绝响应或者该页面没有更新" % responseStatus, level=log.ERROR)
        if 'urlId' in request.meta:
            print '下载调度%s' % spider.name
            urlId=request.meta['urlId']
            self.apt.updateUrlDbStatusById(urlId, status=responseStatus)
        else:
            self.apt.updateUrlDbStatusByUrl(request.url, status=responseStatus)
            log.msg("没有urlId，可能是创建下载过程中丢失了，使用url更新访问状态 url:%s" % request.url, level=log.ERROR)
        log.msg("更新url访问状态 url:%s" % request.url, level=log.INFO)
        
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