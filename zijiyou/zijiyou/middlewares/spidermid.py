# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from zijiyou.db.mongoDbApt import MongoDbApt
from scrapy import log
from scrapy.http.request import Request

class DuplicateUrlFilter(object):
    '''
    新产生的ulr请求存入数据库，在访问之后更新其状态
    '''
    mon=None
    urlDump=None
    colName="CrawlUrl"
    def __init__(self):
        '''init the dump of url which request successful'''
        if self.mon== None:
            self.mon=MongoDbApt()
        if self.urlDump !=None:
            return
        self.urlDump=[]
        queJson={"status":{"$lt":201}}
        results=self.mon.findByDictionaryAndSort(self.colName, queJson, None)
        for result in results:
            if "url" in result:
                self.urlDump.append(result["url"])
        log.msg("初始化urlDump. length of the dump=%s" % len(self.urlDump), level=log.INFO)

    def process_spider_output(self, response, result, spider):
        '''drop the request which appear in urlDump'''
        newResult=[]
        counter=0
        for p in result:
            counter+=1
            if isinstance(p, Request):
                if p.url and (p.url in self.urlDump):
                    log.msg("排除重复 url=%s" % p.url, level=log.INFO)
                    continue
                else:
                    newResult.append(p)
            else:
                newResult.append(p)
        if len(newResult)<counter:
            log.msg("排重数量：%s" % (counter-len(newResult)), level=log.INFO)
        return newResult
        
    def process_spider_input(self, response, spider):
        responseStatus=response.status
        if responseStatus  in range(199,305) :
            dupUrl=response.url
            if not dupUrl in self.urlDump:
                log.msg("new url=%s" % dupUrl, level=log.INFO)
                self.urlDump.append(dupUrl)
        
        