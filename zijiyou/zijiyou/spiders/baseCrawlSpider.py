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
#from zijiyou.db.mongoDbApt import MongoDbApt
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
        crawlUrls = self.apt.findUrlmd5sForDupfilterFromUrlDb()
        dtLoad=datetime.datetime.now()
        log.msg('爬虫排重库完成Url加载.从UrlDb加载%s个；加载数据时间花费：%s' %(len(crawlUrls),dtLoad-dtBegin), level=log.INFO)
        #更新策略
        now = datetime.datetime.now()
        for p in crawlUrls:
            #判断是否是到达需要重新爬取的时刻，若需要重新爬取，则不放入dump中
            if 'updateInterval' in p and p['status'] in [200, 304] and now-datetime.timedelta(days=p["updateInterval"]) > p["dateTime"]:
#                url=p["url"]
#                callBackFunctionName=p["callBack"]
#                pagePriority=p["priority"]
#                meta={}
#                headers={}
#                if 'reference' in p :
#                    meta['reference'] = p['reference']
#                headers['If-Modified-Since'] = self.getGMTFormatDate(p['dateTime'])
#                req=self.makeRequestWithMeta(url, callBackFunctionName=callBackFunctionName, meta=meta, priority=pagePriority, headers=headers)
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
        # load the recentRequest from db
        dtBegin=datetime.datetime.now()
        self.apt=OnlineApt()
        pendingUrls = self.getStartUrls() 
        dtRecentReq=datetime.datetime.now()
        pendingRequest=[]
        log.msg('%s爬虫恢复：完成数据库recentequest加载，时间花费：%s,recentequest数量=%s' % (self.name,dtRecentReq-dtBegin,len(pendingUrls)), level=log.INFO)
            
        if pendingUrls and len(pendingUrls)>0:
            maxInitRequestSize=settings.get('MAX_INII_REQUESTS_SIZE',1000)
            while len(pendingUrls) > maxInitRequestSize:
                pendingUrls.pop(0)
            log.msg('第一个url : %s' % pendingUrls[0], level=log.INFO)
                
            for p in pendingUrls:
                url=p["url"]
                callBackFunctionName=p["callBack"]
                pagePriority=p["priority"]
                meta={}
                headers={}
                if 'reference' in p :
                    meta['reference'] = p['reference']
                if self.updateStrategy in p:
                    meta[self.updateStrategy]=p[self.updateStrategy]
                    headers['If-Modified-Since'] = self.getGMTFormatDate(p['dateTime'])
#                req=self.makeRequestWithMeta(url, callBackFunctionName=callBackFunctionName, meta=meta, priority=pagePriority, headers=headers)
                req=self.makeRequest(url, callBackFunctionName=callBackFunctionName, urlId=p['_id'],priority=pagePriority)
                pendingRequest.append(req)
            dtPendingReq=datetime.datetime.now();
            log.msg("爬虫%s恢复：初始化pendingRequest，时间花费：%s，数量=%s" % (self.name,dtPendingReq-dtBegin,len(pendingRequest)),level=log.INFO)
        else:
            log.msg("爬虫%s的pendingRequest为空，交由scrapy从startUrl开始" % self.name,level=log.ERROR)
        log.msg("爬虫%s完成恢复" % self.name,level=log.ERROR)
        return pendingRequest
        
    def getStartUrls(self): #spiderName=None,colName=None
        """
        查询recent requests
        """
        log.msg("%s爬虫恢复： 查询recentequest" % self.name ,level=log.INFO)
        try:
            #未被下载或下载失败的url
            pendingUrl=self.apt.getPendingUrlsByStatusAndSpiderName(self.name)
            log.msg("未被爬取的pending长度为：%s" % len(pendingUrl), level=log.INFO)
            #获得下载过的Url，以便实现更新策略
            updateUrl=self.apt.getUrlsForUpdatestrategy(self.name)
            log.msg("需要判断是否更新的pending长度为：%s" % len(updateUrl), level=log.INFO)
            #过滤掉已经爬完但并不需要更新或是更新时间未到的记录
            now = datetime.datetime.now()
            updateUrl = filter(lambda p:not (p["status"] in [200, 304] and p["updateInterval"] and now-datetime.timedelta(days=p["updateInterval"]) < p["dateTime"]),updateUrl)
            log.msg("需要更新的pending长度为：%s" % len(updateUrl), level=log.INFO)
            log.msg("为updateUrl添加更新策略标志位", level=log.INFO)
            #在updateUrl的每一项加updateStrategy：itemCollectionName,若url不是Item页，则设置为None
            for p in updateUrl:
                itemCollectionName = None
                for v in self.itemRegex:
                    if re.search(v['regex'], p['url']):
                        itemCollectionName=v['itemCollectionName']
                        break
                #验证数据库是否和类型配置对应
                if itemCollectionName and not itemCollectionName in self.dbCollecions:
                    raise NotConfigured('Response的type不能对应数据表！请检查配置文件spiderConfig的type配置：%s' % itemCollectionName)
                p[self.updateStrategy] = itemCollectionName

            pendingUrl.extend(updateUrl)
            log.msg('总的pending长度为%s, 如下：' % len(pendingUrl), log.DEBUG)            
            for i in pendingUrl:
                log.msg(i['url'], log.DEBUG)
            return pendingUrl
        except (IOError,EOFError):
            log.msg("查数据库异常" ,level=log.ERROR)
            return []

    
    def baseParse(self, response):
        '''解析主逻辑'''
        reqs = []
        if not self.hasInit:
            self.hasInit=True
            log.msg('爬虫%s 在第一次的baseParse中拦截，执行initRequest，进行爬虫恢复' %self.name, level=log.INFO)
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
        pageResponse.setdefault('headers', response.headers)
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
        try:
            links = link_extractor.extract_links(response)
        except Exception ,e:
            log.msg('Exception:%s' % str(e),level=log.DEBUG)
            log.msg('参数：%s' % extra, level=log.DEBUG)
        log.msg('从%s抽取到的链接:%s' % (response.url,links), level=log.DEBUG)
        return links

    def extractRequests(self, response, pagePriority, callBackFunctionName=None, **extra): 
        '''
        抽取新链接，排重，保存新有效链接，为有效链接创建Request
        '''
        links = self.extractLinks(response, **extra)
        #排重
        newLinks=[]
        for p in links:
            md5=getFingerPrint(p)
            if md5 in self.urlDump:
                continue
            newLinks.append(p)
            #保存新url
            self.urlDump.add(md5)
            urlItem={"url":p.url,"md5":md5,"callBack":callBackFunctionName,
                     "spiderName":self.name,"reference":response.url,
                     "status":1000,"priority":pagePriority,"dateTime":datetime.datetime.now()}
            urlId = self.apt.saveNewUrl(urlItem)
            
        reqs = [self.makeRequest(link.url, callBackFunctionName=callBackFunctionName,urlId=urlId,priority=pagePriority) for link in newLinks]
        return reqs

    def makeRequest(self, url, callBackFunctionName=None,urlId=None,meta={}, **kw): 
        '''
        创建Request
        '''
        if not urlId:
            raise NotConfigured('爬虫%s创建Request的url%s没有提供id，将导致无法更新url的状态' % (self.name,url))
        if(callBackFunctionName != None):
            kw.setdefault('callback', self.functionDic[callBackFunctionName])
        meta={'urlId':urlId}
        kw.setdefault('meta',meta)
        return Request(url, **kw)

    def getGMTFormatDate(self, date):
        week=date.strftime('%w')
        day=date.strftime('%d')
        month = date.strftime("%m")
        d = date.strftime(' %Y %H:%M:%S GMT')
        gmt = self.weekMap[week] + ', ' + day + ' ' + self.monthMap[month] + d
        return gmt
