# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''

from scrapy import log
from scrapy.conf import settings
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib_exp.crawlspider import CrawlSpider, Rule
from scrapy.exceptions import NotConfigured
from scrapy.http import Request
from zijiyou.db.mongoDbApt import MongoDbApt
from zijiyou.items.cookies import cookies
from zijiyou.items.itemLoader import ZijiyouItemLoader
from zijiyou.items.zijiyouItem import PageDb
from zijiyou.spiders.spiderConfig import spiderConfig
import datetime
import re


class BaseCrawlSpider(CrawlSpider):
    '''
    基础spider，负责从数据库中取得高优先级url，重新开始spider
    所有spider的父类
    '''
    allowed_domains = ["daodao.com"]
    start_urls = []
    rules = [Rule(r'.*', 'baseParse')]
    
    #最近一次的spider断点
    pendingUrl=[]
    pendingRequest=[]
    #parse函数字典
    functionDic={}
    #普通页 regex
    normalRegex = None
    #item页 regexx
    itemRegex = None
    #数据库操作类
    mongoApt=None
    #验证数据库是否和type配置对应
    dbCollecions=[]
    hasInit=False

    def __init__(self, *a, **kw):      
        super(BaseCrawlSpider, self).__init__(*a, **kw)
        
        self.CrawlDb=settings.get('CRAWL_DB')
        self.ResponseDb=settings.get('RESPONSE_DB')
        if not self.CrawlDb or not self.ResponseDb:
            log.msg('没有配置CRAWL_DB！，请检查settings', level=log.ERROR)
            raise NotConfigured
        self.functionDic["parseItem"]=self.parseItem
        self.dbCollecions=settings.get('DB_COLLECTIONS', [])
        if(not self.initConfig()):
            log.msg('爬虫配置文件加载失败！', level=log.INFO)
            raise NotConfigured
        
    def getStartUrls(self,spiderName=None,colName=None):
        """
        查询recent requests
        """
        try:
            #查数据库
            if not colName:
                colName="UrlDb" #CrawlUrl
            queJson={"status":{"$gte":400}}
            if spiderName:
                queJson['spiderName']=spiderName
            sortField="priority"
            self.pendingUrl=self.mongoApt.findByDictionaryAndSort(colName, queJson, sortField)
            return self.pendingUrl
        except (IOError,EOFError):
            log.msg("查数据库异常" ,level=log.ERROR)
            return None

    def initConfig(self):
        print '初始配置 initConfig'
        log.msg('初始配置 initConfig', level=log.INFO)
        config = spiderConfig[self.name]
        if config and config['startUrls'] and 'allowedDomains' in config and 'normalRegex' in config and 'itemRegex' in config: 
            self.start_urls = config['startUrls']
            self.allowed_domains = config['allowedDomains']
            self.normalRegex = config['normalRegex']
            self.itemRegex = config['itemRegex']
            return True
        else:
            log.msg("spider配置异常，缺少必要的配置信息。爬虫名:%s" % self.name, level=log.ERROR)
            return False

    def initRequest(self):
        '''
        initiate the functionDictionary and request
        '''
        print '初始化Request：initiateRequest'
        # load the recentRequest from db
        if not self.mongoApt:
            log.msg("self.mongoApt为空，初始化mongod链接，并查询recentequest" ,level=log.INFO)
            self.mongoApt=MongoDbApt()
            pendingRrls = self.getStartUrls(spiderName=self.name,colName=self.CrawlDb)
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
                    reference=None
                    if 'reference' in p :
                        reference=p['reference']
                    req=self.makeRequest(url, callBackFunctionName=callBackFunctionName,reference=reference,priority=pagePriority)
                    self.pendingRequest.append(req)
                log.msg("爬虫%s获得pendingRequest，数量=%s" % (self.name,len(self.pendingRequest)),level=log.INFO)
            else:
                log.msg("爬虫%s 的pendingRequest为空，交由scrapy从startUrl启动" % self.name,level=log.ERROR)

    def baseParse(self, response):
        '''start to parse response link'''
        reqs = []
        
        if not self.hasInit:
            self.hasInit=True
            if self.pendingRequest and len(self.pendingRequest)>0:
                reqs.extend(self.pendingRequest)
                log.msg('从数据库查询的url开始crawl，len(pendingRequest)= %s' % len(self.pendingRequest), log.INFO)
            else:
                log.msg('没有从数据库获得合适的url，将从stat_url开始crawl' , log.INFO)
        
        log.msg('解析开始link: %s' % response.url, log.INFO)
        dtBegin=datetime.datetime.now()
        #普通页link
        for v in self.normalRegex:
            reqs.extend(self.extractRequests(response, v['priority'], allow = v['regex']))
        
        normalNum = len(reqs)
#        log.msg("%s parse 产生 普通页 url 数量：%s" % (response.url, len(reqs)), level=log.INFO)
 
        '''item页link'''
        for v in self.itemRegex:
            reqs.extend(self.extractRequests(response, v['priority'], allow = v['regex']))
        for i in reqs:
            log.msg("%s" % i, level=log.DEBUG)
        itemNum = len(reqs) - normalNum
        item = self.parseItem(response)
        if item:
            reqs.append(item)
        dtEnd=datetime.datetime.now()
        dtInterval=dtEnd - dtBegin
        log.msg("解析完成 %s parse 产生 Item页url数量：%s ,普通页数量:%s ,总数：%s ，花费时间：%s" % (response.url, itemNum,normalNum,len(reqs),dtInterval), level=log.INFO)
        
        return reqs

    def parseItem(self, response):
        '''start to parse parse item'''
        itemCollectionName = None
        for v in self.itemRegex:
            if re.search(v['regex'], response.url):
                itemCollectionName=v['itemCollectionName']
                break
        
        if itemCollectionName == None:
            log.msg("不是item的urlLink：%s" %  response.url, level=log.INFO)
            return None
        #验证数据库是否和type配置对应
        if not itemCollectionName in self.dbCollecions:
            log.msg('Response的type不能对应数据表！请检查配置文件spiderConfig的type配置：%s' % itemCollectionName, level=log.ERROR)
            raise NotConfigured
        
        log.msg('保存item页，类型： %s' % itemCollectionName, level=log.INFO)            
        '''ResponseBody'''
        loader = ZijiyouItemLoader(PageDb(),response=response)
        loader.add_value('spiderName', self.name)
        loader.add_value('url', response.url)
        loader.add_value('itemCollectionName', itemCollectionName)
        loader.add_value('responseBody', response.body_as_unicode())
        loader.add_value('optDateTime', datetime.datetime.now())
        pageResponse = loader.load_item()
        return pageResponse
    
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
        reqs = [self.makeRequest(link.url, callBackFunctionName,response.url, priority=pagePriority) for link in links]
        return reqs

    def makeRequest(self, url, callBackFunctionName=None,reference=None, **kw): 
        '''
        make request, the metaDic indicates the name of call back function
        '''
        if(callBackFunctionName != None):
            kw.setdefault('callback', self.functionDic[callBackFunctionName])
        metaDic={'callBack':callBackFunctionName,
                 'reference':reference}
        kw.setdefault('meta',metaDic)
        return Request(url, cookies = cookies.getCookies(self.name), **kw)
    
    def makeRequestWithMeta(self, url, callBackFunctionName=None,meta=None, **kw):
        '''
        make request, the metaDic indicates the name of call back function
        '''
        if(callBackFunctionName != None):
            kw.setdefault('callback', self.functionDic[callBackFunctionName])
        if meta:
            meta['callBack']=callBackFunctionName
        else:
            meta={'callBack':callBackFunctionName}
        kw.setdefault('meta',meta)
        return Request(url, **kw)