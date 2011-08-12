# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from scrapy.exceptions import NotConfigured
from scrapy.selector import HtmlXPathSelector
from zijiyou.config.spiderConfig import spiderConfig
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
import datetime
import re
import string

class BaseBBSSpider(BaseCrawlSpider):
    '''
    Spider for BBS
    '''
    name ="bbsSpider"
    
    #搜索引擎格式
    seUrlFormat=[]
    maxPageNum=20
    itemPriority=1200
    config=None
    seResultList=[]
    
    def __init__(self,*a,**kw):
        super(BaseBBSSpider,self).__init__(*a,**kw)
        self.config=spiderConfig[self.name]
        requiredConfig = ['homePage', 'firstPageItemRegex', 'maxPageNumXpath', 'pagePattern', 'itemPriority']
        for v in requiredConfig:
            if not v in self.config:
                raise NotConfigured("%s的配置文件没有%s，请检查!" % (self.name, v))
        self.functionDic['baseParse'] = self.baseParse
        self.functionDic['parseItem'] = self.parseItem
        
    def baseParse(self,response):
        print '解析BBS List页结果'
        log.msg('解析BBS List页结果link: %s' % response.url, level=log.INFO)
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
            reqsNormal=self.extractRequests(response, v['priority'], callBackFunctionName = 'baseParse', allow = v['regex'])
            reqs.extend(reqsNormal)
        normalNum = len(reqs)
#        log.msg("%s parse 产生 普通list页 url 数量：%s" % (response.url, len(reqs)), level=log.INFO)
        log.msg("list页", level=log.DEBUG)
        for i in reqs:
            log.msg("%s" % i, level=log.DEBUG)
        
        '''item页link'''
        #抽取第一页链接
        itemReqs = []
        if 'firstPageItemRegex' in self.config:
            reqsItem = self.extractRequests(response, self.config['itemPriority'], callBackFunctionName = 'parseItem', allow = self.config['firstPageItemRegex'])
            itemReqs.extend(reqsItem)
            log.msg("第一页item", level=log.DEBUG)
        for i in itemReqs:
            log.msg("%s" % i, level=log.DEBUG)
            
        log.msg("获得第一页总数量为，%s" % len(itemReqs), level=log.INFO)
        #获得每个item项的总页数(每个帖子的总页数)
        maxPageUrlList = self.getMaxPageUrlList(response)
        #判断总的第一页链接数量和抽取出的总的帖子页数列表的数聊是否相同
        pagesItemLinks = []
        if maxPageUrlList:
            log.msg("开始产生除第一页以外的其他帖子的request", level=log.INFO)
            pagePattern = 'pagePattern'
            if pagePattern in self.config and self.config[pagePattern]:
                pagePattern = self.config[pagePattern]
                for v in maxPageUrlList:
                    log.msg(v, level=log.DEBUG)
                    maxPageNum = None
                    replaceRegex = None
                    maxPageNumRegex = None
                    for pk,pv in pagePattern.items():
                        match = re.search(pk, v, 0)
                        if match and match.group(1):
                            maxPageNum = string.atoi(match.group(1))
                            maxPageNumRegex = pk
                            replaceRegex = pv
                            break
                    
                    if not maxPageNum:
                        log.msg("未能匹配到最大页数，配置文件中%s的 pagePattern配置有问题，请检查配置" % self.name, level=log.ERROR)
                        continue
                    log.msg("最大的页码为:%s" % str(maxPageNum), level=log.INFO)
                    if maxPageNum > 1:
                        #递减到2
                        for i in range(maxPageNum, 1, -1):
                            #替换
                            url = self.config['homePage'] + re.sub(maxPageNumRegex,(replaceRegex % i),v)
                            log.msg(url, level=log.DEBUG)
                            pagesItemLinks.append(self.makeRequest(url, callBackFunctionName='parseItem', reference=response.url, priority=self.config['itemPriority']))
            else:
                log.msg("配置文件中%s没有 pagePattern，请检查配置" % self.name, level=log.ERROR)
        else:
            log.msg("", level=log.ERROR)
        
        itemReqs.extend(pagesItemLinks)
        reqs.extend(itemReqs)
        itemNum = len(itemReqs)
        
        dtEnd=datetime.datetime.now()
        dtInterval=dtEnd - dtBegin
        log.msg("解析完成 %s parse 产生 Item页url数量：%s ,普通页数量:%s ,总数：%s ，花费时间：%s" % (response.url, itemNum,normalNum,len(reqs),dtInterval), level=log.INFO)
        
        return reqs
    
    def getMaxPageUrlList(self, response):
        '''获得每个帖子的总页数'''
        hxs=HtmlXPathSelector(response)
        maxPageUrlValues = None
        maxPageNumXpath = "maxPageNumXpath"
        maxPageNumRegex = "maxPageNumRegex"
        if maxPageNumXpath in self.config and self.config[maxPageNumXpath] and not (maxPageNumRegex in self.config and self.config[maxPageNumRegex]):
            maxPageUrlValues = hxs.select(self.config[maxPageNumXpath]).extract()
        elif maxPageNumXpath in self.config and maxPageNumXpath and maxPageNumRegex in self.config and maxPageNumRegex:
            maxPageUrlValues = hxs.select(self.config[maxPageNumXpath]).re(self.config[maxPageNumRegex])
        else:
            log.msg("爬虫%s配置有误，maxPageNumRegex是必须的，maxPageNumRegex是可选的，" % self.name, level=log.ERROR)
            return None
        
        if not maxPageUrlValues:
            log.msg("所有帖子都只有一页，%s" % response.url, level=log.WARNING)
        else:
            log.msg("总共产生的帖子最大页码链接总数量为：%s" % len(maxPageUrlValues), level=log.INFO)
            for i in maxPageUrlValues:
                log.msg(i, level=log.INFO)
        return maxPageUrlValues
    
SPIDER = BaseBBSSpider()