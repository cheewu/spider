# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
import datetime

from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
from zijiyou.spiders.spiderConfig import spiderConfig
from zijiyou.items.zijiyouItem import ResponseBody,Note
from zijiyou.items.itemLoader import ZijiyouItemLoader
from scrapy.exceptions import NotConfigured
from scrapy.selector import HtmlXPathSelector

class BaseSeSpider(BaseCrawlSpider):
    '''
    Spider for www.daodao.com
    '''
    name ="BaseSeSpider"
    
    #搜索引擎格式
    seUrlFormat=[]
    searchPageNum=5
    itemPriority=1000
    
    def __init__(self,*a,**kw):
        super(BaseSeSpider,self).__init__(*a,**kw)
        
        config=spiderConfig[self.name]
        if not 'seUrlFormat' in config:
            log.msg("baseSeSpider的配置文件没有seUrlFormat!", level=log.ERROR)
            raise NotConfigured        
        self.seUrlFormat=config['seUrlFormat']
        
    def makeRequestByKeywordForSEs(self):
        '''
        由关键字创建SE的请求
        '''
        #load关键字
        reqs=[]
        keyWords=self.mongoApt.findByDictionaryAndSort('KeyWord', {}, 'priority')
        if not keyWords and len(keyWords)<1:
            log.msg("没有关键字！", level=log.ERROR)
            return []        
        for keyWord in keyWords:
            for v in self.seUrlFormat:
                format=v['format']
                pagePriority=keyWord['priority']
                url=format % keyWord['keyWord'];
                meta={'type':keyWord['type'],
                      'sePageNum':v['sePageNum'],
                      'resultAreaXpath':v['resultAreaXpath'],
                      'resultItemXpath':v['resultItemXpath'],
                      'nextPageAreaXpath':v['nextPageAreaXpath'],
                      'nextPageItemXpath':v['nextPageItemXpath'],
                      'seName':v['seName']}
                request=self.makeRequestWithMeta(url,callBackFunctionName='baseParse',meta=meta,priority=pagePriority)
                reqs.append(request)
        log.msg('生成了%s个关键字搜索请求' % len(reqs), level=log.INFO)
        return reqs
    
    def baseParse(self,response):
        print '解析搜索引擎结果'
        log.msg('解析link: %s' % response.url, log.INFO)
        reqs = []
        
        if not self.hasInit:
            self.hasInit=True
            if self.pendingRequest and len(self.pendingRequest)>0:
                reqs.extend(self.pendingRequest)
                log.msg('从数据库查询的url开始crawl，len(pendingRequest)= %s' % len(self.pendingRequest), log.INFO)
            else:
                log.msg('没有从数据库获得合适的url，将从stat_url开始crawl' , log.INFO)
            seReqs=self.makeRequestByKeywordForSEs()
            if seReqs and len(seReqs)>0:
                reqs.extend(seReqs)
            else:
                log.msg('关键字没有生成任何Request!，请检查配置文件spiderConfig中baseSeSpider的url格式或数据库关键字表',level=log.ERROR)
        #拦截
        if len(reqs)>0:
            log.msg('拦截Request。url： %s' % response.url, log.INFO)
            return reqs
        
        if not (response.meta and len(response.meta)>0):
            log.msg("没有meta的Response，无法进行目标页和下一页的定位：%s" % response.url, level=log.ERROR)
            return reqs
        meta=response.meta
        print meta
        #item页链接请求
        itemsReq=[]
        resultAreaXpath=meta['resultAreaXpath']
        resultItemXpath=meta['resultItemXpath']
        type=meta['type']
        itemMeta={'type':type}
        hxs=HtmlXPathSelector(response)
        resultArea=hxs.select(resultAreaXpath)
        if resultArea:
            links=resultArea.select(resultItemXpath)
            print links
            if links and len(links)>0:
                for link in links:
                    req=self.makeRequestWithMeta(link, callBackFunctionName='parseItem', meta=itemMeta,priority=self.itemPriority)
                    itemsReq.append(req)
            else:
                log.msg("没有抓取到任何目标页链接！resultItemXpath：%s；url：%s" % (resultItemXpath,response.url), level=log.ERROR)
        else:
            log.msg("没有定位到任何目标区域！resultAreaXpath：%s；url：%s" % (resultAreaXpath,response.url), level=log.ERROR)
        reqs.extend(itemsReq)
        log.msg("%s parse 产生item页的Request数量：%s" % (response.url, len(itemsReq)), level=log.INFO)
        
        #下一页链接
        if not ('sePageNum' in meta and meta['sePageNum']):
            return reqs
        sePageNum=meta['sePageNum']
        listReq=[]
        nextPageAreaXpath=meta['nextPageAreaXpath']
        nextPageItemXpath=meta['nextPageItemXpath']
        nextPageArea=hxs.select(nextPageAreaXpath)
        if nextPageArea:
            links=nextPageArea.select(nextPageItemXpath)
            print links
            if links and len(links)>0:
                for link in links:
                    req=self.makeRequestWithMeta(link, callBackFunctionName='baseParse', meta=meta,priority=10)
                    listReq.append(req)
            else:
                log.msg("没有抓取到任何下一页链接！resultItemXpath：%s；url：%s" % (resultItemXpath,response.url), level=log.ERROR)
        else:
            log.msg("没有定位到任何下一页区域！resultAreaXpath：%s；url：%s" % (resultAreaXpath,response.url), level=log.ERROR)
        reqs.extend(listReq)
        log.msg("%s parse 产生下一页的Request数量：%s" % (response.url, len(listReq)), level=log.INFO)

        return reqs
    
    def parseItem(self,response):
        print '解析搜索目标页'
        
        items=[]
        contentType=''
        log.msg('保存item页，类型： %s' % contentType, level=log.INFO)            
        #ResponseBody
        loader = ZijiyouItemLoader(ResponseBody(),response=response)
        loader.add_value('spiderName', self.name)
        loader.add_value('pageUrl', response.url)
        loader.add_value('type', contentType)
        loader.add_value('content', response.body_as_unicode())
        loader.add_value('dateTime', datetime.datetime.now())
        loader.add_value('status', 100)
        responseBody = loader.load_item()
        items.append(responseBody)
                
        return items
    
SPIDER = BaseSeSpider()