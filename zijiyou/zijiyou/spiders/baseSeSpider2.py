# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from scrapy.exceptions import NotConfigured
from scrapy.selector import HtmlXPathSelector
from zijiyou.common.extractText import Extracter
from zijiyou.config.spiderConfig import spiderConfig
from zijiyou.db.spiderApt import OnlineApt
from zijiyou.items.itemLoader import ZijiyouItemLoader
from zijiyou.items.zijiyouItem import Page, Article
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
import datetime
import re
import string
import urllib

class BaseSeSpider2(BaseCrawlSpider):
    '''
    搜素引擎爬虫
    '''
    name = "baseSeSpider2"
    
    #搜索引擎格式
    seUrlFormat = []
    maxPageNum = 10
    itemPriority = 1000
    config = None
    
    def __init__(self, *a, **kw):
        super(BaseSeSpider2, self).__init__(*a, **kw)
        self.config = spiderConfig[self.name]
        if not 'seUrlFormat' in self.config:
            log.msg("baseSeSpider的配置文件没有seUrlFormat!", level=log.ERROR)
            raise NotConfigured("baseSeSpider的配置文件没有seUrlFormat!")
        self.functionDic['baseParse'] = self.baseParse
        self.functionDic['parseItem'] = self.parseItem
        self.seUrlFormat = self.config['seUrlFormat']
        self.specailField = ['content', 'publishDate']#,'content'
        #在下一页取得的Field
        self.nextPageField = ['content']
        self.articleMetaName = 'Article'
        self.urlPatternMeta = 'urlPattern'
        self.ext = Extracter()
        
    def clearUrlDb(self):
        '''
        清空搜索引擎数据
        '''
        log.msg("开始清空搜索引擎数据" , level=log.INFO)
#        itemCount = self.apt.getUncompelitedSeUrlNumber(self.name)
#        self.apt.removeUncompelitedSeUrl(self.name)
#        log.msg("成功清除未完成的item和搜索引擎item页：共%s个" % itemCount , level=log.INFO)
        
        listCount = self.apt.getCompelitedSeListUrl(self.name)
        self.apt.removeCompelitedSeListUrl(self.name)
        log.msg("清除已经完成的搜索引擎list页：%s" % listCount , level=log.INFO)
        
    def makeFirstPageRequestByKeywordForSEs(self):
        '''
        由关键字创建SE的请求
        '''
        log.msg("开始生成关键字第一页搜索请求", level=log.INFO)
        
        #load关键字
        keyWords = self.apt.findKerwordsForSespider()
        if not keyWords and len(keyWords) < 1:
            log.msg("没有关键字！", level=log.ERROR)
            return []
        counterFirstPageNum = 0
        for keyword in keyWords:
            for v in self.seUrlFormat:
                #设置默认值
                format = v['format']
                encodeType = v['encode']
                word = keyword['keyWord']
#                if word[:3] == codecs.BOM_UTF8:
#                    word = word[3:]
                try:
                    encodeWords = urllib.quote(word.encode(encodeType))
                    pagePriority = keyword['priority']
                    url = format % (encodeWords, 1)
                    meta = {'itemCollectionName':keyword['itemCollectionName'],
                          'sePageNum':keyword['pageNumber'],
                          'priority':keyword['priority'],
                          'resultItemLinkXpath':v['resultItemLinkXpath'],
                          'totalRecordXpath':v['totalRecordXpath'],
                          'totalRecordRegex':v['totalRecordRegex'],
                          'seName':v['seName'],
                          'homePage':v['homePage'],
                          'reference':None}
                    meta[self.urlPatternMeta] = format % (encodeWords, '')
                    self.saveUrl(url, isNeedUpdateUrldump=False, isNeedSavetoDb=True, referenceUrl=v['homePage'], meta=meta, priority=pagePriority)
                    counterFirstPageNum += 1
                except Exception,e:
                    print '生成关键字%s请求的异常%s' % (word,str(e))
                    log.msg('生成关键字%s请求的异常%s' % (word,str(e)) , level=log.ERROR)
        log.msg('生成了%s个关键字搜索请求' % counterFirstPageNum, level=log.INFO)
    
    def makeListRequestByFirstPageForSEs(self, response, pageSize=10):
        '''
        生成后续搜素list页请求
        '''
        totalRecord = 0
        urlPattern = response.meta[self.urlPatternMeta]
        response.meta[self.urlPatternMeta] = None
        meta = response.meta
        meta['reference'] = response.url
        #清除urlPattern
        meta.pop(self.urlPatternMeta)
        curMaxPageNum = self.maxPageNum
        if 'sePageNum' in meta:
            curMaxPageNum = (int) (meta['sePageNum'])
        
        #获得总的记录数
        totalRecordXpath = meta['totalRecordXpath']
        totalRecordRegex = meta['totalRecordRegex']
        hxs = HtmlXPathSelector(response)
        totalRecordValues = None
        if totalRecordXpath and not totalRecordRegex:
            totalRecordValues = hxs.select(totalRecordXpath).extract()
        elif totalRecordXpath and totalRecordRegex:
            totalRecordValues = hxs.select(totalRecordXpath).re(totalRecordRegex)
        else:
            log.msg("配置有误，totalRecordXpath是必须的，totalRecordRegex是可选的，%s" % response.url, level=log.ERROR)
            return NotConfigured("配置有误，totalRecordXpath是必须的，totalRecordRegex是可选的，%s" % response.url)
        if totalRecordValues and len(totalRecordValues) > 0:
            #将字符串中的逗号去掉，并转为整型
            totalRecord = string.atoi(totalRecordValues[0].replace(',', ''))
        else:
            log.msg("抓取不到总搜索结果数，%s" % response.url, level=log.ERROR)
            return None
        totalPage = (totalRecord - 1) / pageSize + 1
        #设定最多爬取页数
        if totalPage > curMaxPageNum:
            totalPage = int(curMaxPageNum)
        if totalPage <= 1:
            log.msg("%s，该关键字只有一个页面结果" % response.url, level=log.INFO)
            return None
        #递减
        for i in range(totalPage, 1, -1):
            url = urlPattern + str(i)
            log.msg('makeRequestByFirstPageForSEs 得到Url：%s' % url, level=log.DEBUG)
            self.saveUrl(url, isNeedUpdateUrldump=False, isNeedSavetoDb=True, referenceUrl=response.url, meta=meta, priority=100)
        log.msg("根据第一页获得搜索结果总数%s，每页%s项，生成的下一页总数为%s" % (totalRecord, pageSize, totalPage), level=log.INFO)
    
    def baseParse(self, response):
        log.msg('解析搜索引擎结果link: %s' % response.url, level=log.INFO)
        reqs = []
        if not self.hasInit:
            self.hasInit = True
            self.apt = OnlineApt()
            #清空搜素引擎中间页面的数据库，防止因爬虫崩溃导致下一次抓取时中间页被错误过滤
            self.clearUrlDb()
            self.makeFirstPageRequestByKeywordForSEs()
            #下载搜素引擎
            if self.keepCrawlingSwitch:
                pendingRequest=self.getPendingRequest()
                reqs.extend(pendingRequest)
            #双倍调度
            self.pendingRequestCounter = 0
            return reqs
        
        #处理下载正确的response
        if response.status == 200:
            if not (response.meta and len(response.meta) > 0):
                log.msg("没有meta的Response，无法进行目标页和下一页的定位：%s" % response.url, level=log.ERROR)
            else:
                meta = response.meta
                meta['reference'] = response.url
                #item页链接请求
                resultItemLinkXpath = meta['resultItemLinkXpath']
                hxs = HtmlXPathSelector(response)
                blocks = hxs.select(resultItemLinkXpath).extract()
                if blocks == None or len(blocks) < 1:
                    log.msg("没有抓取到任何目标页豆腐块！resultItemLinkXpath：%s；url：%s" % (resultItemLinkXpath, response.url), level=log.ERROR)
                else:
                    #第一页搜索结果抽取出总搜索结果数，生成剩余list页的request
                    if self.urlPatternMeta in response.meta:
                        self.makeListRequestByFirstPageForSEs(response)
                    #保存SE提供的url
                    for i in range(len(blocks)-1,-1,-1):
                        self.saveUrl(blocks[i], referenceUrl=response.url, callBackFunctionName='parseItem', meta=meta, priority=1000)
        #计数下载次数
        self.pendingRequestCounter -= 1
        #补充request
        if self.keepCrawlingSwitch and self.pendingRequestCounter <= 0:
            pendingRequest = self.getPendingRequest()
            reqs.extend(pendingRequest)
        return reqs
        
    def parseItem(self, response):
        '''
        解析搜索目标页
        '''
        items = []
        meta = response.meta
        if not ('itemCollectionName' in meta and meta['itemCollectionName']):
            log.msg("没有itemCollectionName的item页！不能确定保存到那张表。url：%s" % response.url, level=log.ERROR)
            return items
        #处理下载正确的response
        if response.status == 200:
            itemCollectionName = meta['itemCollectionName']
            log.msg("保存item页，url:%s" % response.url , level=log.INFO)
            #ResponseBody
            loader = ZijiyouItemLoader(Page(), response=response)
            pageResponse = loader.load_item()
            pageResponse.setdefault('spiderName', self.name)
            pageResponse['status'] = 200
            pageResponse.setdefault('url', response.url)
            pageResponse.setdefault('itemCollectionName', itemCollectionName)
            pageResponse.setdefault('responseBody', response.body_as_unicode().encode('utf-8'))
            pageResponse.setdefault('optDateTime', datetime.datetime.now())
            pageResponse.setdefault('coding', response.encoding)
            pageResponse.setdefault('meta', response.meta)
            items.append(pageResponse)
            
            #解析搜索引擎ArticleItem
            article = self.parseArticleItem(response)    
            if article is not None:
                items.append(article)
        
        #计数下载次数
        self.pendingRequestCounter -= 1
        #补充request
        if self.keepCrawlingSwitch and self.pendingRequestCounter <= 0:
            pendingRequest = self.getPendingRequest()
            items.extend(pendingRequest)
        return items
    
    def parseArticleItem(self, response):
        '''
        解析搜索引擎AcricleItem
        '''
        log.msg("解析搜索引擎AcricleItem", level=log.INFO)
        #判断配置是否正确
        if not self.checkXathConfig(response):
            return None
        article = Article()
        #正文抽取
        title,publishDate,content,imgs,densDic = self.ext.doExtract2(response.body_as_unicode(),threshold=0.4,htmlId=response.url)
        if len(title) >1 and len(content) > 10:
            article.setdefault('title',title)
            article.setdefault('publishDate',publishDate)
            article.setdefault('content',content)
#            article.setdefault('images',imgs)
            article['images'] = imgs
            article.setdefault('url', response.url)
            article.setdefault('spiderName', self.name)
            article.setdefault('optDateTime', datetime.datetime.now())
            article.setdefault('densDic',densDic)
            return article
        else:
            log.msg("博客正文抽取失败，url：%s" % response.url, level=log.WARNING)
        return None
    
    def checkXathConfig(self, response):
        '''判断配置是否正确'''
        if not ('seXpath' in self.config and response.meta['seName'] in self.config['seXpath']):
            log.msg("配置文件中缺少seXpath配置或seXpath中缺少%s的配置" % response.meta['seName'], level=log.ERROR)
            return False
        return True
    
SPIDER = BaseSeSpider2()