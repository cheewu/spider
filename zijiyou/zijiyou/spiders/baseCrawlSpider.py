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
from zijiyou.db.spiderApt import OnlineApt
from zijiyou.items.itemLoader import ZijiyouItemLoader
from zijiyou.items.zijiyouItem import PageDb
#from zijiyou.spiders.offlineCrawl.parse import Parse
import datetime
import re
from zijiyou.common.utilities import getFingerPrint


class BaseCrawlSpider(CrawlSpider):
    '''
    基础spider，负责从数据库中取得高优先级url，重新开始spider
    所有spider的父类
    '''
    allowed_domains = ["daodao.com"]
    start_urls = []
    rules = [Rule(r'.*', 'baseParse')]
    name ="BaseCrawlSpider"
    
    #parse函数字典
    functionDic={}
    #普通页 regex
    normalRegex = None
    #item页 regexx
    itemRegex = None
    #imageXpath 图片xpath
    imageXpath = None
#    #更新策略标志位
#    updateStrategy='updateStrategy'
    #验证数据库是否和type配置对应
    dbCollecions=[]
    hasInit=False
    
    #GMT格式
    weekMap = {'0':'Sun', '1':'Mon', '2':'Tue', '3':'Wed', '4':'Thu', '5':'Fri', '6':'Sat'}
    monthMap = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}

    def __init__(self, *a, **kw):      
        super(BaseCrawlSpider, self).__init__(*a, **kw)
        if(not self.initConfig()):
                raise NotConfigured('爬虫%s配置文件加载失败！'%self.name)
            
    def initConfig(self):
        '''
        初始化加载配置文件
        '''
        log.msg('爬虫%s初始配置信息' %self.name, level=log.INFO)
        #加载setting的配置
        self.dbCollecions=settings.get('DB_COLLECTIONS', [])
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

    def initUrlDupfilterAndgetRequsetForUpdate(self):
        '''
        初始化爬虫排重库，并找出需要更新的网页Reqest
        '''
        log.msg('初始化爬虫%s排重库' % self.name, level=log.INFO)
        self.urlDump=set()
        urlForUpdateStategy=[]
        dtBegin=datetime.datetime.now()
        cursor = self.apt.findUrlsForDupfilter(self.name)
        dtLoad=datetime.datetime.now()
        log.msg('爬虫排重库完成Url加载.从UrlDb加载%s个；加载数据时间花费：%s' %(cursor.count(),dtLoad-dtBegin), level=log.INFO)
        #更新策略
        now = datetime.datetime.now()
        for p in cursor:
            #更新策略
            if 'updateInterval' in p and p['status'] in [200, 304] and now-datetime.timedelta(days=p["updateInterval"]) > p["dateTime"]:
                meta={}
                headers={}
                if 'reference' in p :
                    meta['reference'] = p['reference']
                if self.updateStrategy in p:
                    meta[self.updateStrategy]=p[self.updateStrategy]
                    headers['If-Modified-Since'] = self.getGMTFormatDate(p['dateTime'])
                req=self.makeRequest(p["url"], callBackFunctionName=p["callBack"], urlId=p['_id'],priority=p["priority"])
                urlForUpdateStategy.append(req)
            else:
                self.urlDump.add(p['md5'])
        dtDump=datetime.datetime.now()
        log.msg("爬虫排重库完成初始化. 排重库的容量=%s；初始化Dump花费时间花费：%s" % (len(self.urlDump),dtDump-dtLoad), level=log.INFO)
        log.msg("爬虫%s需要更新的网页数量有%s" % (self.name,len(urlForUpdateStategy)), level=log.INFO)
        return urlForUpdateStategy

    def getPendingRequest(self):
        '''
        爬虫恢复初始化pendingRequest下载请求
        '''
        dtBegin=datetime.datetime.now()
        #查询recent requests
        cursor = self.apt.findPendingUrlsByStatusAndSpiderName(self.name)
        dtRecentReq=datetime.datetime.now()
        pendingRequest=[]
        log.msg('%s爬虫恢复：完成数据库recentequest加载，时间花费：%s,recentequest数量=%s' % (self.name,dtRecentReq-dtBegin,cursor.count()), level=log.INFO)
#            #限制pending_request的长度
#            maxInitRequestSize=settings.get('MAX_INII_REQUESTS_SIZE',1000)
#            while len(pendingUrls) > maxInitRequestSize:
#                pendingUrls.pop(0)
        for p in cursor:
            req=self.makeRequest(p["url"], callBackFunctionName=p["callBack"], urlId=p['_id'],priority=p["priority"])
            pendingRequest.append(req)
        dtPendingReq=datetime.datetime.now();
        log.msg("爬虫%s完成恢复：初始化pendingRequest，时间花费：%s，数量=%s" % (self.name,dtPendingReq-dtBegin,len(pendingRequest)),level=log.INFO)
        return pendingRequest
    
    def baseParse(self, response):
        '''解析主逻辑'''
        reqs = []
        if not self.hasInit:
            self.hasInit=True
            log.msg('爬虫%s 在第一次的baseParse中拦截，执行initRequest，进行爬虫恢复' %self.name, level=log.INFO)
            self.apt=OnlineApt()
            pendingRequest=self.getPendingRequest()
            updateRequest= self.initUrlDupfilterAndgetRequsetForUpdate()
            pendingRequest.extend(updateRequest)
            if len(pendingRequest)>0:
                reqs.extend(pendingRequest)
                log.msg('爬虫%s正式启动执行: 从数据库查询的url开始crawl，len(pendingRequest)= %s' % (self.name,len(pendingRequest)), log.INFO)
            else:
                log.msg('爬虫%s正式启动执行：解析startUrl页面' % self.name , log.INFO)
        log.msg('解析开始link: %s' % response.url, log.INFO)
        dtBegin=datetime.datetime.now()
        #普通页link
        for v in self.normalRegex:
            reqsNormal=[]
            if 'region' in v:
                reqsNormal=self.extractRequests(response, v['priority'], allow = v['regex'],restrict_xpaths=v['region'])
            else:
                reqsNormal=self.extractRequests(response, v['priority'], allow = v['regex'])
            reqs.extend(reqsNormal)
        normalNum = len(reqs)
 
        #item页
        for v in self.itemRegex:
            reqsItem=[]
            if 'region' in v:
                reqsItem=self.extractRequests(response, v['priority'], allow = v['regex'],restrict_xpaths=v['region'])
            else:
                reqsItem=self.extractRequests(response, v['priority'], allow = v['regex'])
            reqs.extend(reqsItem)
        itemNum = len(reqs) - normalNum
        items = self.parseItem(response)
        if items and len(items)>0:
            log.msg('得到items，数量：%s'% len(items),level=log.DEBUG)
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
            log.msg("不是item的urlLink：%s" %  response.url, level=log.WARNING)
            return None
        #验证数据库是否和类型配置对应
        if not itemCollectionName in self.dbCollecions:
            log.msg('Response的type不能对应数据表！请检查配置文件spiderConfig的type配置：%s' % itemCollectionName, level=log.ERROR)
            raise NotConfigured
        
        #保存PageDb
        items=[]
        log.msg('保存item页，类型： %s' % itemCollectionName, level=log.INFO)         
        loader = ZijiyouItemLoader(PageDb(),response=response)
        pageResponse = loader.load_item()
        pageResponse.setdefault('itemCollectionName', itemCollectionName)
        pageResponse.setdefault('spiderName', self.name)
        pageResponse.setdefault('url', response.url)
        pageResponse.setdefault('responseBody', (response.body_as_unicode()).encode('utf-8'))
        pageResponse.setdefault('optDateTime', datetime.datetime.now())
        pageResponse.setdefault('coding', response.encoding)
#        pageResponse.setdefault('headers', response.headers)
        items.append(pageResponse)


#        #解析item
#        dtParseItemBegin=datetime.datetime.now()
#        item=self.itemParser.parseItem(spiderName=self.name, itemCollectionName=itemCollectionName, response=response)
#        dtParseItemEnd=datetime.datetime.now()
#        dtCost=dtParseItemEnd-dtParseItemBegin
#        log.msg('解析item时间花费：%s' % dtCost, level=log.INFO)
#        if item:
#            #测试图像下载
#            if item.has_key('imageUrls'):
#                print '测试图像下载，加入2个imgurls'
#                item['imageUrls']=['http://images3.ctrip.com/images/uploadphoto/photo/0318/636632.jpg','http://images3.ctrip.com/images/uploadphoto/photo/0318/636633.jpg']
#            items.append(item)
#            pageResponse['status']=200
            
        return items

    def extractLinks(self, response, **extra): 
        """ 
        抽取链接
        """
        link_extractor = SgmlLinkExtractor(**extra)
        links = link_extractor.extract_links(response)
        log.msg('从%s抽取到的链接:%s' % (response.url,links), level=log.DEBUG)
        return links

    def extractRequests(self, response, pagePriority, callBackFunctionName=None, **extra): 
        '''
        抽取新链接，排重，保存新有效链接，为有效链接创建Request
        '''
        links = self.extractLinks(response, **extra)
        reqs=[]
        dtBegin=datetime.datetime.now()
        for p in links:
            req=self.makeRequest(p.url,referenceUrl=response.url, callBackFunctionName=callBackFunctionName,priority=pagePriority)
            if req != None:
                reqs.append(req)
        dtEnd=datetime.datetime.now()
        log.msg('对%s个新url排重，重复%s，时间花费%s' % (len(links),(len(links)-len(reqs)),(dtEnd-dtBegin)), level=log.DEBUG)
        return reqs

    def makeRequest(self, url, referenceUrl=None,callBackFunctionName=None,meta={},priority=1, **kw): 
        '''
        排重 保存url到数据库 创建Request返回。如果重复，则返回None
        '''
        #排重
        url=url.strip()
        originUrl=None
        if 'originUrl' in meta and meta['originUrl'] !=None:
            originUrl=meta['originUrl']
            log.msg('对原始url排重 %s' % originUrl, level=log.DEBUG)
        #有originalurl的，对originalurl作为排重url
        md5=None
        if originUrl:
            md5=getFingerPrint(inputs=[originUrl.strip()],isUrl=True)
        else:
            md5=getFingerPrint(inputs=[url],isUrl=True)
        if not md5 or md5 in self.urlDump:
            return None
        self.urlDump.add(md5)
        #保存url到数据库
        urlItem={"url":url,"md5":md5,"callBack":callBackFunctionName,
                 "spiderName":self.name,"reference":referenceUrl,
                 "status":1000,"priority":priority,"dateTime":datetime.datetime.now()}
        if originUrl:
            urlItem['originUrl']=originUrl
        urlId = self.apt.saveNewUrl(urlItem)
        
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
