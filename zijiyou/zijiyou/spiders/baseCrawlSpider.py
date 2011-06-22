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
from zijiyou.config.spiderConfig import spiderConfig
from zijiyou.db.mongoDbApt import MongoDbApt
from zijiyou.items.itemLoader import ZijiyouItemLoader
from zijiyou.items.zijiyouItem import PageDb
from zijiyou.spiders.offlineCrawl.parse import Parse
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
    name ="BaseCrawlSpider"
    
    #最近一次的spider断点
    pendingUrl=[]
    pendingRequest=[]
    #parse函数字典
    functionDic={}
    #普通页 regex
    normalRegex = None
    #item页 regexx
    itemRegex = None
    #imageXpath 图片xpath
    imageXpath = None
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
            log.msg('爬虫配置文件加载失败！' , level=log.ERROR)
            raise NotConfigured
        self.itemParser=Parse()
        
    def getStartUrls(self,spiderName=None,colName=None):
        """
        查询recent requests
        """
        try:
            #查数据库
            if not colName:
                colName="UrlDb" #CrawlUrl
            queJson={"$or":[{"status":{"$gte":400}}, {"status":200, "updateInterval":{"$exists":True}}]}
            if spiderName:
                queJson['spiderName']=spiderName
            sortField="priority"
            self.pendingUrl=self.mongoApt.findByDictionaryAndSort(colName, queJson, sortField)
            log.msg("更新策略过滤前pending长度为：%s" % len(self.pendingUrl), level=log.INFO)
            #过滤掉已经爬完但并不需要更新或是更新时间未到的记录
            now = datetime.datetime.now()
            self.pendingUrl = filter(lambda p:not (p["status"] == 200 and p["updateInterval"] and now-datetime.timedelta(days=p["updateInterval"]) < p["dateTime"]),self.pendingUrl)
            log.msg("更新策略过滤后pending长度为：%s" % len(self.pendingUrl), level=log.INFO)
            for i in self.pendingUrl:
                log.msg(i['url'], log.DEBUG)
            return self.pendingUrl
        except (IOError,EOFError):
            log.msg("查数据库异常" ,level=log.ERROR)
            return []

    def initConfig(self):
        log.msg('爬虫%s初始配置信息spiderConfig' %self.name, level=log.INFO)
        config = spiderConfig[self.name]
        if config and config['startUrls'] and 'allowedDomains' in config and 'normalRegex' in config and 'itemRegex' in config: 
            self.start_urls = config['startUrls']
            self.allowed_domains = config['allowedDomains']
            self.normalRegex = config['normalRegex']
            self.itemRegex = config['itemRegex']
            #获得imageXpath 非必须
            if 'imageXpath' in config:
                self.imageXpath = config['imageXpath']
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
        dtBegin=datetime.datetime.now();
        if not self.mongoApt:
            log.msg("%s爬虫恢复： 查询recentequest" % self.name ,level=log.INFO)
            self.mongoApt=MongoDbApt()
        pendingUrls = self.getStartUrls(spiderName=self.name,colName=self.CrawlDb)
        dtRecentReq=datetime.datetime.now();
        log.msg('%s爬虫恢复：完成数据库recentequest加载，时间花费：%s,recentequest数量=%s' % (self.name,dtRecentReq-dtBegin,len(pendingUrls)), level=log.INFO)
            
        if pendingUrls and len(pendingUrls)>0:
            self.pendingRequest=[]
            maxInitRequestSize=settings.get('MAX_INII_REQUESTS_SIZE',1000)
            while len(pendingUrls) > maxInitRequestSize:
                pendingUrls.pop(0)
            log.msg('第一个url : %s' % pendingUrls[0], level=log.INFO)
                
            for p in pendingUrls:
                url=p["url"]
                callBackFunctionName=p["callBack"]
                pagePriority=p["priority"]
                reference=None
                if 'reference' in p :
                    reference=p['reference']
                req=self.makeRequest(url, callBackFunctionName=callBackFunctionName,reference=reference,priority=pagePriority)
                self.pendingRequest.append(req)
            dtPendingReq=datetime.datetime.now();
            log.msg("爬虫%s恢复：初始化pendingRequest，时间花费：%s，数量=%s" % (self.name,dtPendingReq-dtBegin,len(self.pendingRequest)),level=log.INFO)
        else:
            log.msg("爬虫%s的pendingRequest为空，交由scrapy从startUrl开始" % self.name,level=log.ERROR)
        log.msg("爬虫%s完成恢复" % self.name,level=log.ERROR)

    def baseParse(self, response):
        '''start to parse response link'''
        reqs = []
        
        if not self.hasInit:
            self.hasInit=True
            log.msg('爬虫%s 在第一次的baseParse中拦截，执行initRequest，进行爬虫恢复' %self.name, level=log.INFO)
            self.initRequest();
            if self.pendingRequest and len(self.pendingRequest)>0:
                reqs.extend(self.pendingRequest)
                log.msg('爬虫%s正式启动执行: 从数据库查询的url开始crawl，len(pendingRequest)= %s' % (self.name,len(self.pendingRequest)), log.INFO)
            else:
                log.msg('爬虫%s正式启动执行：解析startUrl页面' % self.name , log.INFO)
        
        log.msg('解析开始link: %s' % response.url, log.INFO)
        dtBegin=datetime.datetime.now()
        #普通页link
        for v in self.normalRegex:
            reqs.extend(self.extractRequests(response, v['priority'], allow = v['regex']))
        
        normalNum = len(reqs)
 
        '''item页link'''
        for v in self.itemRegex:
            reqs.extend(self.extractRequests(response, v['priority'], allow = v['regex']))
        for i in reqs:
            log.msg("解析新得到的url：%s" % i, level=log.DEBUG)
        itemNum = len(reqs) - normalNum
        items = self.parseItem(response)
        if items and len(items)>1:
            reqs.extend(items)
        dtEnd=datetime.datetime.now()
        dtInterval=dtEnd - dtBegin
        log.msg("解析完成 %s parse 产生 Item页url数量：%s ,普通页数量:%s ,总数：%s ，花费时间：%s" % (response.url, itemNum, normalNum, len(reqs),dtInterval), level=log.INFO)
        
        return reqs

    def parseItem(self, response):
        '''start to parse parse item'''
        #识别item页，并解析
        itemCollectionName = None
        for v in self.itemRegex:
            if re.search(v['regex'], response.url):
                itemCollectionName=v['itemCollectionName']
                break
        if itemCollectionName == None:
            log.msg("不是item的urlLink：%s" %  response.url, level=log.INFO)
            return None
        #验证数据库是否和类型配置对应
        if not itemCollectionName in self.dbCollecions:
            log.msg('Response的type不能对应数据表！请检查配置文件spiderConfig的type配置：%s' % itemCollectionName, level=log.ERROR)
            raise NotConfigured
        
        #保存PageDb
        items=[]
        log.msg('保存item页，类型： %s' % itemCollectionName, level=log.INFO)         
        loader = ZijiyouItemLoader(PageDb(),response=response)
        loader.add_value('spiderName', self.name)
        loader.add_value('url', response.url)
        loader.add_value('responseBody', response.body_as_unicode())
        loader.add_value('optDateTime', datetime.datetime.now())
        pageResponse = loader.load_item()
        pageResponse.setdefault('collectionName', itemCollectionName)
        items.append(pageResponse)
        print '测试item的itemCollectionName：%s status:%s' % (pageResponse.get('collectionName'),pageResponse['status'])
        #解析item
        dtParseItemBegin=datetime.datetime.now()
        item=self.itemParser.parseItem(spiderName=self.name, itemCollectionName=itemCollectionName, response=response)
        dtParseItemEnd=datetime.datetime.now()
        dtCost=dtParseItemEnd-dtParseItemBegin
        log.msg('解析item时间花费：%s' % dtCost, level=log.INFO)
        if item:
            #测试图像下载
            if item.has_key('imageUrls'):
                print '测试图像下载，加入2个imgurls'
                item['imageUrls']=['http://images3.ctrip.com/images/uploadphoto/photo/0318/636632.jpg','http://images3.ctrip.com/images/uploadphoto/photo/0318/636633.jpg']
            items.append(item)
            pageResponse['status']=200
        return items
    
#    def parseImageItems(self, response):
#        '''start to parse parse image item'''
#        if not self.imageXpath:
#            return None
#        
#        log.msg("解析图片", level=log.INFO)
#        print "图片解析"
#        imageItems = []
#        hxs = HtmlXPathSelector(response)
#        for xpath in self.imageXpath:
#            imageUrls = hxs.select(xpath).extract()
#            if not imageUrls:
#                continue
#            for url in imageUrls:
#                loader = ZijiyouItemLoader(Image(),response=response)
#                loader.add_value("imageUrl", unicode(str(url), 'utf8'))
#                imageItem = loader.load_item()
#                imageItems.append(imageItem)
#                print imageItemh
#                log.msg(url, level=log.INFO)
#                
#        log.msg("共解析了%s张图片" % len(imageItems), level=log.INFO)
#        return imageItems
    
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
        return Request(url, **kw)
    
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