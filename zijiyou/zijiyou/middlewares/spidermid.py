# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from scrapy import log
from scrapy.http.request import Request
from zijiyou.db.mongoDbApt import MongoDbApt
import datetime

class DuplicateUrlFilter(object):
    '''
    新产生的url进行去重，在访问爬取之后更新其状态
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
        whereJson={"status":{"$lt":301}}
        fieldsJson={'url':1}
        crawlUrls=self.mon.findFieldsAndSort('CrawlUrl', whereJson=whereJson, fieldsJson=fieldsJson)
        responses=self.mon.findFieldsAndSort('ResponseBody', whereJson={}, fieldsJson={'pageUrl':1})
        log.msg('加载排重的urlDump，从CrawlUrl加载%s个；从ResponseBody加载%s个' %(len(crawlUrls),len(responses)), level=log.INFO)
        for p in crawlUrls:
            if "url" in p and (not p['url'] in self.urlDump):
                self.urlDump.append(p['url'])
        for p in responses:
            if "pageUrl" in p and (not p['pageUrl'] in self.urlDump):
                self.urlDump.append(p['pageUrl'])
        log.msg("初始化urlDump. dump的长度=%s" % len(self.urlDump), level=log.INFO)

    def process_spider_output(self, response, result, spider):
        '''drop the request which appear in urlDump'''
        log.msg("对request进行排重",level=log.INFO)
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
    
    
class RequestSaver(object):
    '''
    新产生的url在去重之后进行保存到数据库
    '''            
    mongoApt=None
    colName="CrawlUrl"
    def __init__(self):
        if not self.mongoApt:
            self.mongoApt=MongoDbApt()
            
    def process_spider_output(self, response, result, spider):
        log.msg("将新的request存入数据库",level=log.INFO)
        for req in result:
            if isinstance(req, Request):
                recentReq={"url":"","callBack":None,"status":"","priority":1,"dateTime":datetime.datetime.now()}
                recentReq["url"]=req.url
                meta=req.meta
                if meta and "callBack" in meta:
                    recentReq["callBack"]=req.meta["callBack"]
                recentReq["priority"]=req.priority
                recentReq["status"]=1000
                if spider.name:
                    recentReq["spiderName"]=spider.name
                
                queJson={"url":req.url}
                if not self.mongoApt.isExist(self.colName, queJson):
                    self.mongoApt.saveItem(self.colName,recentReq)
                    log.msg("保存新request：%s" % req.url,level=log.INFO)
        return result
        
        