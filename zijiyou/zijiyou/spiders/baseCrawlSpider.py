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
from zijiyou.common.utilities import getFingerPrint
from zijiyou.config.spiderConfig import spiderConfig
from zijiyou.db.spiderApt import OnlineApt
from zijiyou.items.itemLoader import ZijiyouItemLoader
from zijiyou.items.zijiyouItem import Page, ImageItem
from zijiyou.spiders.offlineCrawl.parse import Parse
import datetime
import re

class BaseCrawlSpider(CrawlSpider):
    '''
    基础spider，负责从数据库中取得高优先级url，重新开始spider
    所有spider的父类
    '''
    allowed_domains = []
    start_urls = []
    rules = [Rule(r'.*', 'baseParse')]
    name ='BaseCrawlSpider'
    handle_httpstatus_list = [302,400,403,404,407,408,500,502,503,504]
    
    #parse函数字典
    functionDic={}
    #普通页 regex
    normalRegex = None
    #item页 regexx
    itemRegex = None
    #imageXpath 图片xpath
    imageXpath = None
    #验证数据库是否和type配置对应
    dbCollecions=[]
    hasInit=False
    #指示是否需要马上解析item
    needParse = False
    
    #GMT格式
    weekMap = {'0':'Sun', '1':'Mon', '2':'Tue', '3':'Wed', '4':'Thu', '5':'Fri', '6':'Sat'}
    monthMap = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}

    def __init__(self, *a, **kw):
        super(BaseCrawlSpider, self).__init__(*a, **kw)
        if not self.initConfig():
                raise NotConfigured('爬虫%s配置文件加载失败！'%self.name)
        if self.needParse:
            self.parser = Parse()
            
    def initConfig(self):
        '''
        初始化加载配置文件
        '''
        log.msg('爬虫%s初始配置信息' %self.name, level=log.INFO)
        #过滤器
        self.urlDump = set()
        #离线调度阀值
        self.pendingRequestCounter=settings.get('PENDING_REQUEST_COUNTER')
        #持续运行爬虫的开关。可以设置为false关掉，当需要测试爬虫的url正则是否能让parser准确地抽取目标url
        self.keepCrawlingSwitch=settings.get('KEEP_CRAWLING_SWITCH')
        self.dbCollecions=settings.get('DB_ITEM_COLLECTIONS')
        #pengdingRequest长度限制
        self.urlIncreasement=settings.get('MAX_INII_REQUESTS_SIZE')
        self.functionDic["parseItem"]=self.parseItem
        self.functionDic['baseParse'] = self.baseParse
        #加载spiderConfig配置
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

    def getRequestsFromCursor(self,cursor,num,isneedDump=True):
        pendingRequestTemp=[]
        for p in cursor:
            meta={}
            if 'meta' in p:
                meta=p['meta']
            if not 'md5' in p:
                log.msg('没有md5的url：%s' % p['url'],level=log.ERROR)
            if isneedDump and p['md5'] in self.urlDump:
                continue
            self.urlDump.add(p['md5'])
            req=self.makeRequest(p["url"],callBackFunctionName=p["callBack"],meta=meta, urlId=p['_id'],priority=p["priority"])#dont_filter = True
#            if not isneedDump:
#                req.dont_filter=True
            if req:
                pendingRequestTemp.append(req)
            #限制pending_request的长度
            if len(pendingRequestTemp)>= num:
                break
        return pendingRequestTemp

    def getPendingRequest(self):
        '''
        爬虫恢复初始化pendingRequest下载请求
        '''
#        dtBegin=datetime.datetime.now()
        #查询recent requests
        pendingRequest=[]
        #调度-2% 为下载异常
        cursorExp = self.apt.findPendingUrlsByStatusAndSpiderName(self.name, statusBegin=800, statusEnd=900)
        numExp = 0.01 * self.urlIncreasement
        pendingRequest.extend(self.getRequestsFromCursor(cursorExp, numExp))
        numExp = len(pendingRequest)
        #调度-2% 为下载失败
        cursorExp = self.apt.findPendingUrlsByStatusAndSpiderName(self.name, statusBegin=301, statusEnd=800)
        numFailed = 0.01 * self.urlIncreasement
        pendingRequest.extend(self.getRequestsFromCursor(cursorExp, numFailed))
        numFailed = len(pendingRequest) - numExp
        #调度剩下的为新url
        cursorNew = self.apt.findPendingUrlsByStatusAndSpiderName(self.name,statusBegin=1000,statusEnd=1001)
        numNew = self.urlIncreasement - numExp - numFailed
        pendingRequest.extend(self.getRequestsFromCursor(cursorNew, numNew))
        numNew = len(pendingRequest) - numFailed - numExp
        #新url不够，则调度异常和失败
        numLast = self.urlIncreasement - len(pendingRequest)
        if numLast > 0 :
            cursorLst = self.apt.findPendingUrlsByStatusAndSpiderName(self.name, statusBegin=301, statusEnd=1000)
            pendingRequest.extend(self.getRequestsFromCursor(cursorLst, numLast))
            numLast = len(pendingRequest) - numNew - numFailed - numExp
#        dtEnd=datetime.datetime.now()
        #重置下载计数器
        self.pendingRequestCounter = settings.get('PENDING_REQUEST_COUNTER')
        if self.pendingRequestCounter > len(pendingRequest):
            self.pendingRequestCounter = len(pendingRequest) - 20
        print "爬虫%s补充request成分：下载异常%s；下载失败：%s ；新url数：%s ；最后补充调度:%s ；pendingRequestCounter:%s ;url补充总数：%s" % (self.name,numExp,numFailed,numNew,numLast,self.pendingRequestCounter,len(pendingRequest))
        log.msg("爬虫%s补充request成分：下载异常%s；下载失败：%s ；新url数：%s ；最后补充调度:%s ；pendingRequestCounter:%s ;url补充总数：%s" % (self.name,numExp,numFailed,numNew,numLast,self.pendingRequestCounter,len(pendingRequest)),level=log.INFO)
        return pendingRequest
    
    def baseParse(self, response):
        '''解析主逻辑'''
        print '下载完成，状态值:%s，开始解析%s ' % (response.status,response.url)
        reqs = []
        #初始化操作
        if not self.hasInit:
            self.hasInit=True
            self.apt=OnlineApt()
#            self.initUrlDupfilter()
            if self.keepCrawlingSwitch:
                pendingRequest=self.getPendingRequest()
                reqs.extend(pendingRequest)
            #初始双倍加载
            self.pendingRequestCounter = 0

        #处理下载正常的response
        if response.status == 200:
            log.msg('解析开始link: %s' % response.url, log.INFO)
            dtBegin=datetime.datetime.now()
            #普通页link
            counterNor = 0
            for v in self.normalRegex:
                linksNormal=[]
                meta={'multitype':'multitype' in v and v['multitype'] or False}
                if 'region' in v:
                    linksNormal=self.extractLinks(response,allow = v['regex'],restrict_xpaths = v['region'])
                else:
                    linksNormal=self.extractLinks(response,allow = v['regex'])
                counterNor += len(linksNormal)
                #保存新url
                for newlink in linksNormal:
                    url=newlink.url
                    self.saveUrl(url, isNeedUpdateUrldump=False, isNeedSavetoDb=True, referenceUrl=response.url,meta=meta, priority=v['priority'])
            
            #item页
            counterItem = 0
            for v in self.itemRegex:
                linksItem=[]
                multitype = 'multitype' in v and v['multitype'] or False
                if 'region' in v:
                    linksItem=self.extractLinks(response,allow = v['regex'],restrict_xpaths = v['region'])
                else:
                    linksItem=self.extractLinks(response,allow = v['regex'])
                counterItem += len(linksItem)
                #保存新url
                for newlink in linksItem:
                    url=newlink.url
                    if multitype:
                        self.saveUrl(url, isNeedUpdateUrldump=False, isNeedSavetoDb=True, referenceUrl=response.url,meta={'multitype':multitype}, priority=v['priority'])
                    else:
                        self.saveUrl(url, isNeedUpdateUrldump=False, isNeedSavetoDb=True, referenceUrl=response.url,callBackFunctionName='parseItem',meta={'multitype':multitype}, priority=v['priority'])
            #item
            meta = response.meta
            if 'multitype' in meta and meta['multitype'] or not 'multitype' in meta : 
                items = self.parseItem(response)
                if items and len(items)>0:
                    log.msg('得到items，数量：%s'% len(items),level=log.DEBUG)
                    reqs.extend(items)
            dtEnd=datetime.datetime.now()
            dtInterval=dtEnd - dtBegin
            log.msg("解析完成 %s parse 产生 Item页url数量：%s ,普通页数量:%s ,总数：%s ，花费时间：%s" % (response.url, counterItem, counterNor, len(reqs),dtInterval), level=log.INFO)
        
        #计数下载次数
        self.pendingRequestCounter -= 1
        #补充request
        if self.keepCrawlingSwitch and self.pendingRequestCounter <= 0:
            pendingRequest = self.getPendingRequest()
            reqs.extend(pendingRequest)
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
        loader = ZijiyouItemLoader(Page(),response=response)
        pageResponse = loader.load_item()
        pageResponse.setdefault('itemCollectionName', itemCollectionName)
        pageResponse.setdefault('spiderName', self.name)
        pageResponse.setdefault('url', response.url)
        pageResponse.setdefault('responseBody', (response.body_as_unicode()).encode('utf-8'))
        pageResponse.setdefault('optDateTime', datetime.datetime.now())
        pageResponse.setdefault('coding', response.encoding)
        items.append(pageResponse)

        #解析item
        if self.needParse:
            item=self.parser.parseItem(spiderName=self.name, itemCollectionName=itemCollectionName, response = response, responseBody = response.body_as_unicode(), pageid = response.url)
            if item:
                #若有图片，判断是否需要对图片补充domain
                if 'imageUrls' in item:
                    newimglist = []
                    for img in item['imageUrls']:
                        if not re.search('http://', img):
                            newimg = "http://" + self.allowed_domains[0] + img
                        else:
                            newimg = img
                        newimglist.append(newimg)
                    item['imageUrls'] = newimglist
                #装箱
                newitem = ImageItem()
                #临时
                if itemCollectionName == 'ImageItem':
                    newitem = ImageItem()
                for k,v in item.items():
                    newitem[k] = v
                items.append(newitem)
                log.msg('在线解析item成功,url:%s' % response.url,level= log.INFO)
                print '在线解析item成功,url:%s' % response.url
                pageResponse['status']=200
                
        #计数下载次数
        self.pendingRequestCounter -= 1
        #补充request
        if self.keepCrawlingSwitch and self.pendingRequestCounter <= 0:
            pendingRequest = self.getPendingRequest()
            items.extend(pendingRequest)
        return items

    def extractLinks(self, response, **extra): 
        """ 
        抽取链接
        """
        link_extractor = SgmlLinkExtractor(**extra)
        links = link_extractor.extract_links(response)
        log.msg('从%s抽取到的链接:%s' % (response.url,len(links)), level=log.DEBUG)
        return links

#    def extractRequests(self, response, pagePriority, callBackFunctionName=None, **extra): 
#        '''
#        抽取新链接，排重，保存新有效链接，为有效链接创建Request
#        '''
#        links = self.extractLinks(response, **extra)
#        reqs=[]
#        dtBegin=datetime.datetime.now()
#        for p in links:
#            req=self.makeRequest(p.url,referenceUrl=response.url, callBackFunctionName=callBackFunctionName,priority=pagePriority)
#            if req:
#                reqs.append(req)
#        dtEnd=datetime.datetime.now()
#        if len(links)>0:
#            log.msg('对%s个新url排重，重复%s，时间花费%s' % (len(links),(len(links)-len(reqs)),(dtEnd-dtBegin)), level=log.INFO)
#        return reqs
#
#    def checkDupAndSaveUrl(self,url,isNeedUpdateUrldump=False,isNeedSavetoDb=True,referenceUrl=None,callBackFunctionName=None, meta={},urlId=None,priority=1):
#        """
#        保存url。先排重，排重时可指定是否需要更新排重库；重复的不入库以降低数据库IO压力。返回(isnotDup,urlId,md5)
#        """
#        if url:
#            #url特征
#            md5 = None
#            if 'originUrl' in meta:
#                md5=getFingerPrint(inputs=[meta['originUrl'].strip()], isUrl=True)
#            else:
#                md5=getFingerPrint(inputs=[url.strip()])
#            if not md5 in self.urlDump:
#                #更新urlDump
#                if isNeedUpdateUrldump:
#                    self.urlDump.add(md5)
#                #保存url到数据库
#                urlItem={"url":url,"md5":md5,"callBack":callBackFunctionName,
#                         "spiderName":self.name,"reference":referenceUrl,
#                         "status":1000,"priority":priority,"dateTime":datetime.datetime.now()}
#                if len(meta)>0:
#                    urlItem['meta']=meta
#                if 'originUrl' in meta:
#                    urlItem['originUrl']=meta['originUrl']
#                #保存到数据库
#                urlId = None
#                if isNeedSavetoDb:
#                    urlId = self.apt.saveNewUrl(self.name,urlItem=urlItem)
#                return (True,urlId,md5)
#        return (None,None,None)
    
    def saveUrl(self,url,isNeedUpdateUrldump=False,isNeedSavetoDb=True,referenceUrl=None,callBackFunctionName=None, meta={},urlId=None,priority=1):
        """
        保存url。先排重，排重时可指定是否需要更新排重库；重复的不入库以降低数据库IO压力。返回(isnotDup,urlId,md5)
        """
        if url:
            #url特征
            md5 = None
            if 'originUrl' in meta:
                md5=getFingerPrint(inputs=[meta['originUrl'].strip()], isUrl=True)
            else:
                md5=getFingerPrint(inputs=[url.strip()])
            #保存url到数据库
            urlItem={"url":url,"md5":md5,"callBack":callBackFunctionName,
                         "spiderName":self.name,"reference":referenceUrl,
                         "status":1000,"priority":priority,"dateTime":datetime.datetime.now()}
            if len(meta)>0:
                urlItem['meta']=meta
            if 'originUrl' in meta:
                urlItem['originUrl']=meta['originUrl']
            self.apt.saveNewUrl(self.name,urlItem=urlItem)
            
    def makeRequest(self, url,referenceUrl=None,callBackFunctionName=None,meta={},urlId=None,priority=1, **kw): 
        '''
        排重 保存url到数据库 创建Request返回。如果重复，则返回None
        '''
        if not urlId:
            raise NotConfigured('爬虫%s创建Request的url%s没有提供id，将导致无法更新url的状态' % (self.name,url))
        if(callBackFunctionName != None):
            kw.setdefault('callback', self.functionDic[callBackFunctionName])
        meta['urlId']=urlId
        kw.setdefault('meta',meta)
        kw.setdefault('priority',priority)
        return Request(url, **kw)

    def getGMTFormatDate(self, date):
        week=date.strftime('%w')
        day=date.strftime('%d')
        month = date.strftime("%m")
        d = date.strftime(' %Y %H:%M:%S GMT')
        gmt = self.weekMap[week] + ', ' + day + ' ' + self.monthMap[month] + d
        return gmt
