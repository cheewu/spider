# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from scrapy.http.request import Request
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
import datetime
import re

class BaseBBSSpider2(BaseCrawlSpider):
    '''
    Spider for BBS V2 每次通过分析帖子ID 自动拼接出想要的URL
    '''
    name ="bbsSpider2"
    
    def printRequest(self,r,right=False):
        if isinstance(r,Request) :
            if right:
                log.msg('right', level=log.ERROR)
            log.msg('url %s' % r.url, level=log.ERROR)
            log.msg('method %s' % r.method, level=log.ERROR)
            log.msg('header %s' % r.headers, level=log.ERROR)
            log.msg('body %s' % r.body, level=log.ERROR)
            log.msg('meta %s' % r.meta, level=log.ERROR)
            if right:
                log.msg('rightOver', level=log.ERROR)
        else:
            print 'not Request %s ' % r.url
    
    def baseParse(self, response):
        '''start to parse response link'''
#        self.printRequest(response.request,right=True)
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
        log.msg('%s解析开始link: %s' % (self.name,response.url), log.INFO)
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
 
        '''item页link'''
        for v in self.itemRegex:
            links=[]
            # 抽item的link
            if 'region' in v:
                links = self.extractLinks(response, allow = v['regex'],restrict_xpaths=v['region'])
            else:
                links = self.extractLinks(response, allow = v['regex'])
            if len(links)<1:
                log.msg('从%s中没有抽取到item的link。reg：%s;region:%s' % (response.url,v['regex'],v['region']), level=log.WARNING)
            # 拼凑item的新link
            for link in links:
                match=re.search(v['itemTidRegex'], link.url, 0)
                if match and match.group(1):
                    tid=match.group(1)
                    newLink=v['itemPrintPageFormat'] % tid
                    log.msg("拼凑item打印链接：%s" %newLink, level=log.DEBUG)
                    newReq=self.makeRequest(newLink,reference=response.url,priority=v['priority'])
#                    self.printRequest(newReq)
                    reqs.append(newReq)
                else:
                    log.msg("抽出的link:%s 没有发现tid，不能拼凑出新链接。请检查正则是否有误： linkXpath：%s、tid正则:%s" %(link.url,v['regex'],v['itemTidRegex']), level=log.ERROR)
                
        itemNum = len(reqs) - normalNum
        items = self.parseItem(response)
        if items and len(items)>0:
            log.msg('得到items，数量：%s'% len(items),level=log.DEBUG)
            reqs.extend(items)
        dtEnd=datetime.datetime.now()
        dtInterval=dtEnd - dtBegin
        log.msg("解析完成 %s parse 产生 Item页url数量：%s ,普通页数量:%s ,总数：%s ，花费时间：%s" % (response.url, itemNum, normalNum, len(reqs),dtInterval), level=log.INFO)
        
        return reqs
    
    
SPIDER = BaseBBSSpider2()