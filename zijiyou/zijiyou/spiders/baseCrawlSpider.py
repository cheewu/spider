# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''

from scrapy import log
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib_exp.crawlspider import CrawlSpider
from scrapy.http import Request
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from scrapy.contrib_exp.crawlspider import Rule
import datetime
import re

from zijiyou.db.mongoDbApt import MongoDbApt
from zijiyou.spiders.spiderConfig import spiderConfig
from zijiyou.items.zijiyouItem import ResponseBody
from zijiyou.items.itemLoader import ZijiyouItemLoader

class BaseCrawlSpider(CrawlSpider):
    '''
    基础spider，负责从数据库中取得高优先级url，重新开始spider
    所有spider的父类
    '''
    allowed_domains = ["daodao.com"]
    start_urls = []
    rules = [Rule(r'.*', 'myParse')]
    
    colName="CrawlUrl"
    pendingRequest=[]
    functionDic={}
    '''普通页 regex'''
    normalRegex = None
    '''item页 regex'''
    itemRegex = None
    mongoApt=None
    hasInit=False

    def __init__(self, *a, **kw):      
        super(BaseCrawlSpider, self).__init__(*a, **kw)
          
        self.functionDic["parseItem"]=self.parseItem
        if(not self.initConfig()):
            print 'not self.initConfig()'
            log.msg('not self.initConfig()', level=log.INFO)
            raise NotConfigured
        
    def getStartUrls(self,spiderName=None,colName=None):
        """
        查询recent requests
        """
        try:
            #查数据库
            if colName:
                self.colName=colName
            recentRrls=[]
            queJson={"status":{"$gte":300}}
            if spiderName:
                queJson['spiderName']=spiderName
            sortField="priority"
            recentRrls=self.mongoApt.findByDictionaryAndSort(self.colName, queJson, sortField)
            return recentRrls
        except (IOError,EOFError):
            log.msg("查数据库异常" ,level=log.ERROR)
            return None

    def initConfig(self):
        print '初始配置 initConfig'
        log.msg('初始配置 initConfig', level=log.INFO)
        config = spiderConfig[self.name]
        if config and config['startUrls'] and config['allowedDomains'] and config['normalRegex'] and config['itemRegex']: 
            self.start_urls = config['startUrls']
            self.allowed_domains = config['allowedDomains']
            self.normalRegex = config['normalRegex']
            self.itemRegex = config['itemRegex']
            return True
        else:
            log.msg("there is sth wrong with the config of spider:%s" % self.name, level=log.ERROR)
            return False

    def initRequest(self):
        '''
        initiate the functionDictionary and request
        '''
        print 'initiateRequest'
        # load the recentRequest from db
        if not self.mongoApt:
            print 'self.mongoApt为空，初始化mongod链接，并查询recentequest'
            log.msg("self.mongoApt为空，初始化mongod链接，并查询recentequest" ,level=log.INFO)
            self.mongoApt=MongoDbApt()
            pendingRrls = self.getStartUrls(spiderName=self.name)
            if pendingRrls and len(pendingRrls)>0:
                self.pendingRequest=[]
                maxInitRequestSize=settings.get('MAX_INII_REQUESTS_SIZE',1000)
                while len(pendingRrls) > maxInitRequestSize:
                    pendingRrls.pop(0)
                log.msg('开始crawl，第一个url : %s' % pendingRrls[0], level=log.INFO)
                
                for p in pendingRrls:
                    url=p["url"]
                    callBackFunctionName=p["callBack"]
                    pagePriority=p["priority"]
                    req=self.makeRequest(url, callBackFunctionName,priority=pagePriority)
                    self.pendingRequest.append(req)
                
                log.msg("获得pendingRequest，数量=%s" % len(self.pendingRequest),level=log.INFO)
            else:
                log.msg("pendingRequest为空，交由scrapy从startUrl启动" ,level=log.ERROR)

    def myParse(self, response):
        '''start to parse response link'''
        print '解析link'
        
        if not self.hasInit:
            self.initRequest()
            self.hasInit=True
            if self.pendingRequest and len(self.pendingRequest)>0:
                log.msg('从数据库查询的url开始crawl，len(pendingRequest)= %s' % len(self.pendingRequest), log.INFO)
                return self.pendingRequest
        
        log.msg('解析link: %s' % response.url, log.INFO)
        reqs = []
        '''普通页link'''
        for v in self.normalRegex:
            reqs.extend(self.extractRequests(response, v['priority'], allow = v['regex']))
           
        log.msg("%s parse 产生 普通页 url 数量：%s" % (response.url, len(reqs)), level=log.INFO)
 
        '''item页link'''
        for v in self.itemRegex:
            reqs.extend(self.extractRequests(response, v['priority'], allow = v['regex']))
            
        item = self.parseItem(response)
        if item:
            reqs.append(item)
        return reqs

    def parseItem(self, response):
        '''start to parse parse item'''
        contentType = None
        for v in range(len(self.itemRegex)):
            if re.search(self.itemRegex[v]['regex'], response.url):
                if v == 0:
                    contentType = "Attraction"
                elif v == 1:
                    contentType = "Note"
                elif v == 2:
                    contentType = "CommonSense"
                    
        if contentType == None:
            log.msg("the url is not item link：%s" %  response.url, level=log.INFO)
            return None
        
        log.msg('start to parse item, the type of content is %s' % contentType, level=log.INFO)            
        '''ResponseBody'''
        loader = ZijiyouItemLoader(ResponseBody(),response=response)
        loader.add_value('spiderName', self.name)
        loader.add_value('pageUrl', response.url)
        loader.add_value('type', contentType)
        loader.add_value('content', response.body_as_unicode())
        loader.add_value('dateTime', datetime.datetime.now())
        loader.add_value('status', 100)
        responseBody = loader.load_item()
        return responseBody
    
    def extractLinks(self, response, **extra): 
        """ 
        Extract links from response
        extra - passed to SgmlLinkExtractor
        """
        link_extractor = SgmlLinkExtractor(**extra)
        links = link_extractor.extract_links(response)
        return links

    def extractRequests(self, response, pagePriority, callBackFunctionName=None, **extra): 
        '''
        extract links identified by extra, then makeRequests 
        '''
        links = self.extractLinks(response, **extra)
        reqs = [self.makeRequest(link.url, callBackFunctionName, priority=pagePriority) for link in links]
        return reqs

    def makeRequest(self, url, callBackFunctionName=None, **kw): 
        '''
        make request, the metaDic indicates the name of call back function
        '''
        if(callBackFunctionName != None):
            kw.setdefault('callback', self.functionDic[callBackFunctionName])
        metaDic={'callBack':callBackFunctionName}
        kw.setdefault('meta',metaDic)
        return Request(url, **kw)