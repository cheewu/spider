# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from zijiyou.db.mongoDbApt import MongoDbApt
from scrapy import log
from scrapy.http.request import Request
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from scrapy.utils.url import canonicalize_url

import hashlib
import datetime
#import re

class DuplicateUrlFilter(object):
    '''
    新产生的ulr请求存入数据库，在访问之后更新其状态
    '''
#    mon=None
#    urlDump=None
#    colName="CrawlUrl"
    def __init__(self):
        '''init the dump of url which request successful'''
        self.mon=MongoDbApt()
        self.urlDump=set()
        self.colName=settings.get('CRAWL_DB')
        if not self.colName:
            log.msg('没有配置CRAWL_DB！，请检查settings', level=log.ERROR)
            raise NotConfigured
        whereJson={"status":{"$lt":400}}
        fieldsJson={'url':1}#需统一
        log.msg('spider中间件开始从数据库加载CrawlUrl和ResponseBody.url，时间：%s' % datetime.datetime.now(), level=log.INFO)
        crawlUrls=self.mon.findFieldsAndSort('CrawlUrl', whereJson=whereJson, fieldsJson=fieldsJson)
        log.msg('完成CrawlUrl加载，时间：%s' %datetime.datetime.now(), level=log.INFO)
        responses=self.mon.findFieldsAndSort('ResponseBody', whereJson={}, fieldsJson={'pageUrl':1})
        log.msg('完成ResponseBody加载.从CrawlUrl加载%s个；从ResponseBody加载%s个；时间：%s' %(len(crawlUrls),len(responses),datetime.datetime.now()), level=log.INFO)
        for p in crawlUrls:
            self.urlDump.add(p['url'])
        for p in responses:
            self.urlDump.add(p['pageUrl'])
        log.msg("spider中间件完成初始化urlDump. dump的长度=%s；时间：%s" % (len(self.urlDump),datetime.datetime.now()), level=log.INFO)
    
    def process_spider_output(self, response, result, spider):
        '''drop the request which appear in urlDump'''
        log.msg("开始排重", level=log.INFO)
        newResult=[]
        counter=0
        for p in result:
            counter+=1
            if isinstance(p, Request):
                if p.url:
                    if p.url in self.urlDump:
                        log.msg("排除重复 url=%s" % (p.url), level=log.DEBUG)
                        continue
                    else:
                        #更新urlDump
                        self.urlDump.add(p.url)
                        #保存到数据库
                        recentReq={"url":p.url,"callBack":None,"reference":None,"status":1000,"priority":p.priority,"dateTime":datetime.datetime.now()}
                        meta=p.meta
                        if not meta:
                            log.msg('错误：meta为空，url:%s' % p.url, level=log.ERROR)
                        if meta and 'callBack' in meta:
                            recentReq["callBack"]=meta["callBack"]
                        else:
                            log.msg('错误：meta.callBack为空，url:%s' % p.url, level=log.ERROR)
                        if meta and 'reference' in meta:
                            recentReq["reference"]=meta["reference"]
                        else:
                            log.msg('错误：meta.reference为空，url:%s' % p.url, level=log.ERROR)
                        recentReq["spiderName"]=spider.name
                        self.mon.saveItem(self.colName,recentReq)
                        log.msg("保存新request：%s" % p.url,level=log.DEBUG)
                        
                        #放回请求队列
                        newResult.append(p)
            else:
                newResult.append(p)
        if len(newResult)<counter:
            log.msg("url总数量：%s,排重数量：%s，通过(添加到数据库)数量：%s" % (counter,counter-len(newResult),len(newResult)), level=log.INFO)
        else:
            log.msg("排重中间件所有的url均不重复！数量：%s" % len(newResult), level=log.INFO)
        return newResult
        
    def process_spider_input(self, response, spider):
        responseStatus=response.status
        if responseStatus  in range(199,305) :
            dupUrl=response.url
            if not dupUrl in self.urlDump:
                log.msg("new url=%s" % dupUrl, level=log.INFO)
                self.urlDump.add(dupUrl)
        
class SaveNewRequestUrl(object):
    '''
    保存新产生的url
    '''
    mongoApt=None
    colName="CrawlUrl"
    def __init__(self):
        if not self.mongoApt:
            self.mongoApt=MongoDbApt()
        
    def process_spider_output(self, response, result, spider):
        counterNew=0
        counterExist=0
        newResult=[]
        for p in result:
            newResult.append(p)
            if isinstance(p, Request):
                queJson={"url":p.url}
                if not self.mongoApt.isExist(self.colName, queJson):
                    counterNew+=1
                    recentReq={"url":p.url,"callBack":None,"reference":None,"status":1000,"priority":p.priority,"dateTime":datetime.datetime.now()}
                    meta=p.meta
                    if not meta:
                        log.msg('错误：meta为空，url:%s' % p.url, level=log.ERROR)
                    if meta and 'callBack' in meta:
                        recentReq["callBack"]=meta["callBack"]
                    else:
                        log.msg('错误：meta.callBack为空，url:%s' % p.url, level=log.ERROR)
                    if meta and 'reference' in meta:
                        recentReq["reference"]=meta["reference"]
                    else:
                        log.msg('错误：meta.reference为空，url:%s' % p.url, level=log.ERROR)
                    recentReq["spiderName"]=spider.name
                    self.mongoApt.saveItem(self.colName,recentReq)
                    log.msg("保存新request：%s" % p.url,level=log.INFO)
                else:
                    counterExist+=1
                #test
#                urlTest=p.url
#                matches = re.search(r'.*(attraction_review)+.*', urlTest)
#                if not matches:
#                    newResult.append(p)
        
        log.msg("spider中间件保存新url.NewUrl=%s; ExistUrl=%s ; result长度：%s,url:%s" % (counterNew,counterExist,len(newResult),response.url),level=log.INFO)
        return newResult

def getFingerPrint(self,input):
    '''
        指纹
    '''
    hasher=hashlib.sha1()
    hasher.update(canonicalize_url(str(input)))
    fp=hasher.hexdigest()
    return fp