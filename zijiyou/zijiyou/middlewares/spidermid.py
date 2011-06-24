# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from scrapy.http.request import Request
from scrapy.utils.url import canonicalize_url
from zijiyou.db.mongoDbApt import MongoDbApt
from zijiyou.common import utilities
import datetime
import re
#from scrapy.utils.url import canonicalize_url

#import re

class DuplicateUrlFilter(object):
    '''
    新产生的ulr请求存入数据库，在访问之后更新其状态
    '''
    def __init__(self):
        '''init the dump of url which request successful'''
        self.mon=MongoDbApt()
        self.urlDump=set()
        self.CrawlDb=settings.get('CRAWL_DB')
        self.ResponseDb=settings.get('RESPONSE_DB')
        if not self.CrawlDb or not self.ResponseDb:
            log.msg('没有配置CRAWL_DB！，请检查settings', level=log.ERROR)
            raise NotConfigured
        whereJson={"status":{"$lt":400}}
        fieldsJson={'url':1,'md5':1, 'status':1, 'updateInterval':1, 'dateTime':1} #status updateInterval用来判断
        dtBegin=datetime.datetime.now()
        log.msg('spider中间件开始从数据库加载UrlDb' , level=log.INFO)
        crawlUrls=self.mon.findFieldsAndSort(self.CrawlDb, whereJson=whereJson, fieldsJson=fieldsJson)
        dtLoad=datetime.datetime.now()
        log.msg('spider中间件完成Url加载.从CrawlUrl加载%s个；加载数据时间花费：%s' %(len(crawlUrls),dtLoad-dtBegin), level=log.INFO)
        now = datetime.datetime.now()
        for p in crawlUrls:
            if "url" in p :
                #判断是否是到达需要重新爬取的时刻，若需要重新爬取，则不放入dump中
                if 'status' in p and 'updateInterval' in p and 'dateTime' in p and p['status'] in [200, 304] and now-datetime.timedelta(days=p["updateInterval"]) > p["dateTime"]:
                    continue
                self.urlDump.add(p['md5'])
        dtDump=datetime.datetime.now()
        log.msg("spider中间件完成初始化urlDump. dump的长度=%s；初始化Dump花费时间：%s" % (len(self.urlDump),dtDump-dtLoad), level=log.INFO)
    
    def process_spider_output(self, response, result, spider):
        '''drop the request which appear in urlDump'''
        log.msg("开始排重", level=log.INFO)
        newResult=[]
        counter=0
        dtBegin=datetime.datetime.now()
        for p in result:
            counter+=1
            if isinstance(p, Request):
                if p.url:
                    fp=utilities.getFingerPrint(inputs=p.url,isUrl=True)
                    if fp in self.urlDump:
                        log.msg("排除重复 url=%s" % (p.url), level=log.DEBUG)
                        continue
                    else:
                        #更新urlDump
                        self.urlDump.add(fp)
                        
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
                        recentReq['md5']=fp
                        self.mon.saveItem(self.CrawlDb,recentReq)
                        log.msg("保存新request：%s" % p.url,level=log.DEBUG)
                        
                        #放回请求队列
                        newResult.append(p)
            else:
                newResult.append(p)
        dtEnd=datetime.datetime.now()
        if len(newResult)<counter:
            log.msg("url总数量：%s,排重数量：%s，通过(添加到数据库)数量：%s 排重花费时间：%s" % (counter,counter-len(newResult),len(newResult),dtEnd-dtBegin), level=log.INFO)
        else:
            log.msg("排重中间件所有的url均不重复！数量：%s ,排重花费时间：%s" % (len(newResult),dtEnd-dtBegin), level=log.INFO)
        return newResult
        
    def process_spider_input(self, response, spider):
        responseStatus=response.status
        if responseStatus  in range(199,305) :
            dupUrl=response.url
            if not dupUrl in self.urlDump:
                log.msg("警告！spider中间件滤重时没有增加url，是starturl?：%s" % dupUrl, level=log.ERROR)
                self.urlDump.add(dupUrl)
        
class SaveNewRequestUrl(object):
    '''
    保存新产生的url
    '''
    def __init__(self):
        self.mongoApt=MongoDbApt()
        self.CrawlDb=settings.get('CRAWL_DB')
        if not self.CrawlDb :
            log.msg('没有配置CRAWL_DB！，请检查settings', level=log.ERROR)
            raise NotConfigured
                
    def process_spider_output(self, response, result, spider):
        counterNew=0
        counterExist=0
        newResult=[]
        for p in result:
            newResult.append(p)
            if isinstance(p, Request):
                queJson={"url":p.url}
                if not self.mongoApt.isExist(self.CrawlDb, queJson):
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
                    self.mongoApt.saveItem(self.CrawlDb,recentReq)
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

class UrlNormalizer(object):
    '''url normalizer (归一化)'''
    def __init__(self):
        log.msg('UrlNormalizer 中间件初始化', level=log.INFO)
        self.rules = settings.get('URLNORMALIZER_RULES')
        if not self.rules:
            log.msg('没有配置 URLNORMALIZER_RULES！，请检查settings', level=log.WARNING)
    
    def process_spider_output(self, response, result, spider):
        if self.rules:
            log.msg("url normalizer (归一化)", level=log.INFO)
            counter = 0
            newResult = []
            for p in result:
                if isinstance(p, Request): 
                    originUrl = p.url
                    #先进行url标准化
                    tmpUrl = canonicalize_url(originUrl)
                    #按规则的先后顺序进行归一化
                    for k,v in self.rules.items():
                        newUrl = re.sub(k, v, tmpUrl)
                        if not newUrl == tmpUrl:
                            p = p.replace(url=newUrl)
                            tmpUrl = newUrl
                    if not originUrl == p.url:
                        counter += 1
                        log.msg("原来的url：%s, 新的url：%s" % (originUrl, p.url), level=log.DEBUG)
                newResult.append(p)
            log.msg("总共归一化数量为：%s" % counter, level=log.INFO)
        return newResult
        
class UpdateStrategy(object):
    '''
    更新策略
    '''
    def __init__(self):
        self.mongoApt=MongoDbApt()
        
    def process_spider_input(self, response, spider):
        #判断 response中的meta是否有一个标识字段，如 updateStrategy,其字段值不为None时为Response的Item类型，为None时为list页的Response
        if 'updateStrategy' in response.meta and response.meta['updateStrategy']:
            log.msg('进行更新策略，删除DB中的相应的url记录：%s' % response.url, level=log.DEBUG)
            log.msg(response.meta['updateStrategy'], log=log.DEBUG)
            whereJson = {'url':response.url}
            self.mongoApt.remove('PageDb', whereJson)
            self.mongoApt.remove(response.meta['updateStrategy'], whereJson)
