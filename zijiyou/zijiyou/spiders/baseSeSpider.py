# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from scrapy.selector import HtmlXPathSelector
from zijiyou.common.extractText import doExtract, getText
from zijiyou.config.spiderConfig import spiderConfig
from zijiyou.items.itemLoader import ZijiyouItemLoader
from zijiyou.items.zijiyouItem import PageDb, Article
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
import datetime
import re
import string
import time
import urllib

class BaseSeSpider(BaseCrawlSpider):
    '''
    搜素引擎爬虫
    '''
    name ="baseSeSpider"
    
    #搜索引擎格式
    seUrlFormat=[]
    maxPageNum=20
    itemPriority=1200
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
        self.urlPatternMeta = 'urlPattern'
        
    def clearUrlDb(self):
        '''
        清空搜索引擎数据
        '''
        log.msg("开始清空搜索引擎数据" ,level=log.INFO)
        itemCount = self.apt.getUncompelitedSeUrlNumber()
        self.apt.removeUncompelitedSeUrl()
        log.msg("成功清除未完成的item和搜索引擎list页：共%s个" % itemCount ,level=log.INFO)
        
        listCount=self.apt.getCompelitedSeListUrl()
        self.apt.removeCompelitedSeListUrl()
        log.msg("清除已经完成的搜索引擎list页：%s" % listCount ,level=log.INFO)
        log.msg("完成清理搜索引擎数据" ,level=log.INFO)
        
    def makeFirstPageRequestByKeywordForSEs(self):
        '''
        由关键字创建SE的请求
        '''
        log.msg("开始生成关键字第一页搜索请求", level=log.INFO)
        
        #load关键字
        reqs=[]
        keyWords = self.apt.findKerwordsForSespider()
        if not keyWords and len(keyWords)<1:
            log.msg("没有关键字！", level=log.ERROR)
            return []
        for keyWord in keyWords:
            for v in self.seUrlFormat:
                #设置默认值
                format=v['format']
                encodeType=v['encode']
                encodeWords=urllib.quote(keyWord['keyWord'].encode(encodeType))
                pagePriority=keyWord['priority']
                url=format % (encodeWords, 1)
                meta={'itemCollectionName':keyWord['itemCollectionName'],
                      'sePageNum':keyWord['pageNumber'],
                      'priority':keyWord['priority'],
                      'resultItemLinkXpath':v['resultItemLinkXpath'],
                      'nextPageLinkXpath':v['nextPageLinkXpath'],
                      'totalRecordXpath':v['totalRecordXpath'],
                      'totalRecordRegex':v['totalRecordRegex'],
                      'seName':v['seName'],
                      'homePage':v['homePage'],
                      'reference':None}
                meta[self.urlPatternMeta] = format % (encodeWords, '')
                request=self.makeRequestWithMeta(url,callBackFunctionName='baseParse',meta=meta,priority=pagePriority)
                reqs.append(request)
                    
                self.seResultList.append(url)
        log.msg('生成了%s个关键字搜索请求' % len(reqs), level=log.INFO)
        return reqs
    
    def makeRequestByFirstPageForSEs(self, response, pageSize=10):
        if not response or not self.urlPatternMeta in response.meta or not response.meta[self.urlPatternMeta]:
            return None
        
        totalRecord = 0
        urlPattern = response.meta[self.urlPatternMeta]
        response.meta[self.urlPatternMeta] = None
        meta = response.meta
        meta['reference']=response.url
        
        #获得总的记录数
        totalRecordXpath = meta['totalRecordXpath']
        totalRecordRegex = meta['totalRecordRegex']
        hxs=HtmlXPathSelector(response)
        totalRecordValues = None
        if totalRecordXpath and not totalRecordRegex:
            totalRecordValues = hxs.select(totalRecordXpath).extract()
        elif totalRecordXpath and totalRecordRegex:
            totalRecordValues = hxs.select(totalRecordXpath).re(totalRecordRegex)
        else:
            log.msg("配置有误，totalRecordXpath是必须的，totalRecordRegex是可选的，%s" % response.url, level=log.ERROR)
            return None
        if totalRecordValues and len(totalRecordValues) > 0:
            #将字符串中的逗号去掉，并转为整型
            totalRecord = string.atoi(totalRecordValues[0].replace(',', ''))
        else:
            log.msg("抓取不到总搜索结果数，%s" % response.url, level=log.ERROR)
            return None
        totalPage = (totalRecord-1) / pageSize + 1
        #设定最多爬取页数
        if totalPage > self.maxPageNum:
            totalPage = self.maxPageNum
        log.msg("关键字第一页url:%s" % response.url, level=log.INFO)
        log.msg("根据第一页获得搜索结果总数%s，每页%s项，最大的爬取页数为%s，总页数为%s" % (totalRecord, pageSize, self.maxPageNum, totalPage), level=log.INFO)
        if totalPage <= 1:
            log.msg("%s，该关键字只有一个页面结果" % response.url, level=log.INFO)
            return None
        log.msg("开始生成关键字除第一页剩余的所有页面搜索请求", level=log.INFO)
        reqs=[]
        #递减
        for i in range(totalPage, 1, -1):
            url = urlPattern + str(i)
#            log.msg('makeRequestByFirstPageForSEs 得到Url：%s' % url, level=log.INFO)#debug
            request=self.makeRequestWithMeta(url,callBackFunctionName='baseParse',meta=meta,priority=1000)
            reqs.append(request)
#            log.msg('makeRequestByFirstPageForSEs 得到Res：%s' % url, level=log.INFO)#debug
                    
            self.seResultList.append(url)
        return reqs
    
    def baseParse(self,response):
        print '解析搜索引擎结果'
        log.msg('解析搜索引擎结果link: %s' % response.url, level=log.INFO)
        reqs = []
        
        if not self.hasInit:
            self.hasInit=True
            #清空搜素引擎中间页面的数据库，防止因爬虫崩溃导致下一次抓取时中间页被错误过滤
            self.clearUrlDb()
            seReqs=self.makeFirstPageRequestByKeywordForSEs()
            if seReqs and len(seReqs)>0:
                reqs.extend(seReqs)
            else:
                log.msg('关键字没有生成任何Request!，请检查配置文件spiderConfig中baseSeSpider的url格式或数据库关键字表',level=log.ERROR)
                raise NotConfigured
        #拦截第一次解析，提交搜素引擎关键字创建的request
        if len(reqs)>0:
            log.msg('拦截第一次解析，提交搜素引擎关键字创建的request，共%s个' % len(reqs), log.INFO)
            return reqs
        
        if not (response.meta and len(response.meta)>0):
            log.msg("没有meta的Response，无法进行目标页和下一页的定位：%s" % response.url, level=log.ERROR)
            return reqs
        meta=response.meta
        meta['reference']=response.url
        #item页链接请求
        itemsReq=[]
        homePage=meta['homePage']
        resultItemLinkXpath=meta['resultItemLinkXpath']
        hxs=HtmlXPathSelector(response)
        links=hxs.select(resultItemLinkXpath).extract()
        
        #判断是否是第一页搜索结果，是，则抽取出总搜索结果数，计算出总页数，生成剩余页数的request
        if self.urlPatternMeta in response.meta:
            pageLinks = self.makeRequestByFirstPageForSEs(response, len(links))
            if pageLinks:
                reqs.extend(pageLinks)
                log.msg("第一页：%s，生成剩余的搜索页面数为：：%s" % (response.url, len(pageLinks)), level=log.INFO)
            else:
                log.msg("只生成了一页：%s" % response.url, level=log.INFO)
        
        #开始抓取页面上的搜索结果
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
#                log.msg('解析搜素结果页面%s' % (response.url), level=log.INFO) #debug
#                log.msg('meta为%s' % (metaItem), level=log.INFO) #debug
                if metaItem:
                    item = {}
                    for k,v in metaItem.items():
                        item[k] = v[i]
                    if item:
                        meta[self.articleMetaName] = item
            for  i in range(len(links)):
                link = links[i]
                
#                log.msg('%s' % link, level=log.INFO)#debug
#                log.msg('baseParse将抽取的link创建Req Url是：%s' % link, level=log.INFO)#debug
                req=self.makeRequestWithMeta(homePage+link, callBackFunctionName='parseItem', meta=meta,priority=self.itemPriority)
                itemsReq.append(req)
        else:
            log.msg("没有抓取到任何目标页链接！resultItemLinkXpath：%s；url：%s" % (resultItemLinkXpath,response.url), level=log.ERROR)
        
        reqs.extend(itemsReq)
        log.msg("%s parse 产生item页的Request数量：%s" % (response.url, len(itemsReq)), level=log.INFO)
        
        return reqs
    
    def parseItem(self,response):
        '''解析搜索目标页'''
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
        pageResponse = loader.load_item()
        pageResponse.setdefault('spiderName', self.name)
        pageResponse.setdefault('url', response.url)
        pageResponse.setdefault('itemCollectionName', itemCollectionName)
        pageResponse.setdefault('responseBody', response.body_as_unicode().encode('utf-8'))
        pageResponse.setdefault('optDateTime', datetime.datetime.now())
        pageResponse.setdefault('coding', response.encoding)
        pageResponse.setdefault('headers', response.headers)
        
        items.append(pageResponse)
        
        #解析搜索引擎NoteItem
        article = self.parseArticleItem(response)    
        if article:
            items.append(article)
        
        return items
    
    def parseArticleItem(self, response):
        '''解析搜索引擎AcricleItem'''
        log.msg("解析搜索引擎AcricleItem", level=log.INFO)
        #判断配置是否正确
        if not self.checkXathConfig(response):
            return None
        
        xpathItems = self.config['seXpath'][response.meta['seName']]
        hxs=HtmlXPathSelector(response)
        article=Article()
        #添加前一页的field项
        if self.articleMetaName in response.meta:
            for k,v in response.meta[self.articleMetaName].items():
                v = unicode(str(v), 'utf8')
                article.setdefault(k, getText(v))
        #添加下一页的field项
        for k,v in xpathItems.items():
            if k in self.nextPageField:
                value = None
                if not v:
                    values = hxs.extract()
                    value=("".join("%s" % p for p in values)).encode("utf-8")
                else:
                    values = hxs.select(v).extract()
                    value=("-".join("%s" % p for p in values)).encode("utf-8")
                if k in self.specailField:
                    value=self.parseSpecialField(k, value)
                if value:
                    article.setdefault(k, getText(value))
        article.setdefault('url', response.url)
        article.setdefault('spiderName', response.url)
        return article
    
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