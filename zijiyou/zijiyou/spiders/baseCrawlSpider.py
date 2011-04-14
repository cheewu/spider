# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''

from scrapy import log, signals
from scrapy.conf import settings
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib_exp.crawlspider import CrawlSpider
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from zijiyou.db.mongoDbApt import MongoDbApt


class BaseCrawlSpider(CrawlSpider):
    '''
    基础spider，负责从数据库中取得高优先级url，重新开始spider
    所有spider的父类
    '''
    functionDic={}
    
    priorityCounty=10
    priorityArea = 100
    priorityAttraction = 200
    priorityAttractionItem=500
    
    priorityNoteEntry=200
    priorityNote=300
    priorityNoteItem=400
    
    mongoApt=None
    colName="crawlCol"

    def __init__(self): 
        #最近的访问，优先级最高，恢复爬虫时的起始请求。 在schedule中间件存入数据库时会更新它 
        #样例：[{"url":"","callBack":"","status":"","priority":1}]
        log.msg("baseCrawlSpider __init__++++++++++++++++++++++++++++++++++++++++++++++", level=log.INFO) 
        if not self.mongoApt:
            self.mongoApt=MongoDbApt()
        self.recentRequests = []
        dispatcher.connect(self.spiderClosed, signal=signals.spider_closed)
        super(BaseCrawlSpider, self).__init__()

    def __unicode__(self):
        return u'%s' % self.__class__()

    def getStartUrls(self): #_get_start_urls
        """
        查询recent requests
        """ 
        log.msg("getStartUrls++++++++++++++++++++++++++++++++++++++++++++++", level=log.INFO) 
        try:
            #查数据库
            recentRrls=[]
            queJson={"status":"0"}
            sortField="priority"
            recentRrls=self.mongoApt.findByDictionaryAndSort(self.colName, queJson, sortField)
            return recentRrls
        except (IOError,EOFError):
            print "查数据库异常"
            return None

    def start_requests(self):
        '''
        override
        若获得recent requests，则用它启动spider，否则从start_url启动
        '''
        print len(self.rules)
        log.msg("start_requests++++++++++++++++++++++++++++++++++++++++++++++", level=log.INFO) 
        recentRrls = self.getStartUrls()
        if recentRrls:
            log.msg("start_requests1++++++++++++++++++++++++++++++++++++++++++++++", level=log.INFO) 
            reqs = []
            
            maxRecentUrlSize=settings.get('RECENT_URLS_SIZE',3000)
            while len(recentRrls) > maxRecentUrlSize:
                recentRrls.pop(0)
            firstRrl = recentRrls[0]
            log.msg('开始crawl，第一个url : %s' % firstRrl, level=log.INFO)
            
            for p in recentRrls:
                url=p["url"]
                callBackFunctionName=p["callBack"]
                pagePriority=p["priority"]
                req=self.makeRequest(url, callBackFunctionName,priority=pagePriority)
                reqs.append(req)
            log.msg("获得recent requests，数量=%s" % len(reqs),level=log.INFO)
            return reqs
        else:
            log.msg("recent requests为空，交给父类启动" ,level=log.ERROR)
            return super(BaseCrawlSpider, self).start_requests()

    def spiderClosed(self):
        """
        update the recent request list to DB.
        """
        #增加优先级
        log.msg("spiderClosed,start_urls+++%s" % (self.start_urls[0]), level=log.INFO)
        recentRequests=self.recentRequests
        for p in recentRequests:
            p["priority"]=p["priority"]*10
            
        for p in recentRequests:
            whereJson={"url":p["url"]}
            updateJson={"priority":p["priority"]}
            self.mongoApt.updateItem(self.colName,whereJson,updateJson)
        self.recentRequests=[]
        print len(self.rules)
        log.msg("recentRequests 入数据库：%s" %len(recentRequests), level=log.INFO)
        
        #重启
        # Scheduler.clear_pending_requests(self)
        # Scheduler.open_spider(self)

    def extractLinks(self, response, **extra): 
        """ 
        Extract links from response
        extra - passed to SgmlLinkExtractor
        """
        link_extractor = SgmlLinkExtractor(**extra)
        links = link_extractor.extract_links(response)
        return links

    def extractRequests(self, response, pagePriority,callBackFunctionName, **extra): 
        '''
        extract links identified by extra, then makeRequests 
        '''
        links = self.extractLinks(response, **extra)
        reqs = [self.makeRequest(link.url, callBackFunctionName,priority=pagePriority) for link in links]
        return reqs

    def makeRequest(self, url,callBackFunctionName, **kw): 
        '''
        make request, the metaDic indicates the name of call back function
        '''
        metaDic={'callBack':callBackFunctionName}
        kw.setdefault('callback', self.functionDic[callBackFunctionName])
        kw.setdefault('meta',metaDic)
        return Request(url, **kw)
    
    
    
