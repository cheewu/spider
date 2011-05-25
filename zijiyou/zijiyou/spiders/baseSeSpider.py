# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log, signals
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from scrapy.selector import HtmlXPathSelector
from scrapy.xlib.pydispatch import dispatcher
from zijiyou.items.itemLoader import ZijiyouItemLoader
from zijiyou.items.zijiyouItem import PageDb, Article
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
from zijiyou.spiders.offlineCrawl.extractText import doExtract, getText
from zijiyou.spiders.spiderConfig import spiderConfig
import datetime
import re
import time
import urllib




class BaseSeSpider(BaseCrawlSpider):
    '''
    Spider for www.daodao.com
    '''
    name ="baseSeSpider"
    
    #搜索引擎格式
    seUrlFormat=[]
    searchPageNum=20
    itemPriority=1000
    config=None
    seResultList=[]
    
    def __init__(self,*a,**kw):
        super(BaseSeSpider,self).__init__(*a,**kw)
        
        self.CrawlDb=settings.get('CRAWL_DB')
        if not self.CrawlDb :
            log.msg('没有配置CRAWL_DB！，请检查settings', level=log.ERROR)
            raise NotConfigured
        self.config=spiderConfig[self.name]
        if not 'seUrlFormat' in self.config:
            log.msg("baseSeSpider的配置文件没有seUrlFormat!", level=log.ERROR)
            raise NotConfigured
        self.functionDic['baseParse'] = self.baseParse
        self.seUrlFormat=self.config['seUrlFormat']
        self.specailField=['content','publishDate']#,'content'
        self.nextPageField=['content'] #在下一页取得的Field
        self.articleMetaName = 'Article'
        self.initRequest()
        dispatcher.connect(self.onSeSpiderClosed, signal=signals.spider_closed)
        
    def onSeSpiderClosed(self):
        '''清空数据库中的SeSpider中的搜索页列表'''
        log.msg('开始清空数据库中的SeSpider中的搜索页列表，长度：%s' % len(self.seResultList), level=log.INFO)
        if len(self.seResultList)>0:
            whereJson={}
            for url in self.seResultList :
                whereJson['url']=url
                self.mongoApt.remove(self.CrawlDb,whereJson)
            log.msg('清空数据库中的SeSpider中的搜索链接数量：%s' % len(self.seResultList), level=log.INFO)
        self.seResultList=[]
        
    def makeRequestByKeywordForSEs(self):
        '''
        由关键字创建SE的请求
        '''
        log.msg("开始生成关键字搜索请求", level=log.INFO)
        
        #load关键字
        reqs=[]
        keyWords=self.mongoApt.findByDictionaryAndSort('KeyWord', {}, 'priority')
        if not keyWords and len(keyWords)<1:
            log.msg("没有关键字！", level=log.ERROR)
            return []
        for keyWord in keyWords:
            for v in self.seUrlFormat:
                #设置默认值
                if not keyWord['pageNumber']:
                    keyWord['pageNumber'] = self.searchPageNum
                if not keyWord['priority']:
                    keyWord['priority'] = self.itemPriority
                    
                for i in range(1, keyWord['pageNumber']+1):
                    format=v['format']
                    encodeType=v['encode']
                    encodeWords=urllib.quote(keyWord['keyWord'].encode(encodeType))
                    pagePriority=keyWord['priority']
                    url=format % (encodeWords, i)
#                    print url
                    meta={'itemCollectionName':keyWord['itemCollectionName'],
                          'sePageNum':keyWord['pageNumber'],
                          'resultItemLinkXpath':v['resultItemLinkXpath'],
                          'nextPageLinkXpath':v['nextPageLinkXpath'],
                          'seName':v['seName'],
                          'homePage':v['homePage'],
                          'reference':None}
                    request=self.makeRequestWithMeta(url,callBackFunctionName='baseParse',meta=meta,priority=pagePriority)
                    reqs.append(request)
                    
                    self.seResultList.append(url)
        log.msg('生成了%s个关键字搜索请求' % len(reqs), level=log.INFO)
        return reqs
    
    def baseParse(self,response):
        print '解析搜索引擎结果'
        log.msg('解析搜索引擎结果link: %s' % response.url, level=log.INFO)
        reqs = []
        
        if not self.hasInit:
            self.hasInit=True
            if self.pendingRequest and len(self.pendingRequest)>0:
                reqs.extend(self.pendingRequest)
                log.msg('从数据库查询的url开始crawl，len(pendingRequest)= %s' % len(self.pendingRequest), log.INFO)
            else:
                log.msg('没有从数据库获得合适的url，将从stat_url开始crawl' , level=log.INFO)
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
        meta['reference']=response.url
#        print meta
        #item页链接请求
        itemsReq=[]
        homePage=meta['homePage']
        print homePage
        resultItemLinkXpath=meta['resultItemLinkXpath']
        hxs=HtmlXPathSelector(response)
        links=hxs.select(resultItemLinkXpath).extract()
        
        if links and len(links)>0:
            metaItem = {}
            #判断配置是否正确
            if self.checkXathConfig(response):
                xpathItems = self.config['seXpath'][response.meta['seName']]
                for k,v in xpathItems.items():
                    if k in self.nextPageField:
                        continue
                    values = hxs.select(v).extract()
                    if not values or len(values) != len(links):
                        log.msg("%s未抓取到或是抓取到的数量没有和link数一样，可能是xpath有问题" % k, log.WARNING)
                        continue
                    for i in range(len(values)):
                        values[i] = values[i].encode('utf-8')
                        if k in self.specailField:
                            values[i]=self.parseSpecialField(k, values[i])
                    metaItem[k] = values
                
            for  i in range(len(links)):
                link = links[i]
                
                log.msg("%s"%link, log.INFO)
                if metaItem:
                    item = {}
                    for k,v in metaItem.items():
                        item[k] = v[i]
                    if item:
                        meta[self.articleMetaName] = item
                req=self.makeRequestWithMeta(link, callBackFunctionName='parseItem', meta=meta,priority=self.itemPriority)
                itemsReq.append(req)
        else:
            log.msg("没有抓取到任何目标页链接！resultItemLinkXpath：%s；url：%s" % (resultItemLinkXpath,response.url), level=log.ERROR)
        reqs.extend(itemsReq)
        log.msg("%s parse 产生item页的Request数量：%s" % (response.url, len(itemsReq)), level=log.INFO)

        return reqs
    
    def parseItem(self,response):
        '''解析搜索目标页'''
        print '解析搜索目标页'
        log.msg("解析搜索目标页", level=log.INFO)
        items=[]
        
        meta=response.meta
        if not ('itemCollectionName' in meta and meta['itemCollectionName']):
            log.msg("没有itemCollectionName的item页！不能确定保存到那张表。url：%s" % response.url, level=log.ERROR)
            return items
        
        itemCollectionName=meta['itemCollectionName']
        log.msg("保存item页，类型:%s"%str(itemCollectionName) , level=log.INFO)
        #ResponseBody
        loader = ZijiyouItemLoader(PageDb(),response=response)
        loader.add_value('spiderName', self.name)
        loader.add_value('url', response.url)
        loader.add_value('itemCollectionName', itemCollectionName)
        loader.add_value('responseBody', response.body_as_unicode())
        loader.add_value('optDateTime', datetime.datetime.now())
        pageResponse = loader.load_item()
        items.append(pageResponse)
        
        #解析搜索引擎NoteItem
        article = self.parseArticleItem(response)    
        if article:
            items.append(article)
        
        return items
    
    def parseArticleItem(self, response):
        '''解析搜索引擎AcricleItem'''
        log.msg("解析搜索引擎NoteItem", level=log.INFO)
        #判断配置是否正确
        if not self.checkXathConfig(response):
            return None
        
        xpathItems = self.config['seXpath'][response.meta['seName']]
        hxs=HtmlXPathSelector(response)
        loader = ZijiyouItemLoader(Article(),response=response)
        #添加前一页的field项
        if self.articleMetaName in response.meta:
            for k,v in response.meta[self.articleMetaName].items():
                v = unicode(str(v), 'utf8')
                loader.add_value(k, getText(v))
        #添加下一页的field项
        for k,v in xpathItems.items():
            if k in self.nextPageField:
                values = hxs.select(v).extract()
                value=("-".join("%s" % p for p in values)).encode("utf-8")
                if k in self.specailField:
                    value=self.parseSpecialField(k, value)
                if value:
                    loader.add_value(k, getText(value))
        loader.add_value('url', response.url)
        loader.add_value('spiderName', self.name)
        noteItem = loader.load_item()
        return noteItem
    
    def parseSpecialField(self,name,content):
        '''
        特殊处理的字段解析
        '''
        if not name or not content:
            return None
        if name == 'publishDate':
            value = re.search(r"(\d{4}年\d{2}月\d{2}日)|(\d{4}-\d{2}-\d{2})", content)
            if value:
                return value.group(0)
            else:
                return time.strftime("%Y年%m月%d日")
        if name == 'content':
            print '正文抽取'
            mainText = doExtract(content,threshold=False)
#            print mainText
            return mainText
        
    
    def checkXathConfig(self, response):
        '''判断配置是否正确'''
        if not ('seXpath' in self.config and response.meta['seName'] in self.config['seXpath']):
            log.msg("配置文件中缺少seXpath配置或seXpath中缺少%s的配置" % response.meta['seName'], level=log.ERROR)
            return False
        return True
    
SPIDER = BaseSeSpider()