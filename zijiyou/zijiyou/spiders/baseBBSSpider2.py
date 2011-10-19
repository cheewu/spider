# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from zijiyou.db.spiderApt import OnlineApt
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
import re

class BaseBBSSpider2(BaseCrawlSpider):
    '''
    Spider for BBS V2 每次通过分析帖子ID 自动拼接出想要的URL
    '''
    name ="bbsSpider2"
    
    def baseParse(self, response):
        '''start to parse response link'''
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
            log.msg('%s解析开始link: %s' % (self.name,response.url), log.INFO)
            #普通页link
            counterNor = 0
            for v in self.normalRegex:
                linksNormal=[]
                if 'region' in v:
                    linksNormal=self.extractLinks(response,allow = v['regex'],restrict_xpaths = v['region'])
                else:
                    linksNormal=self.extractLinks(response,allow = v['regex'])
                counterNor += len(linksNormal)
                #保存新url
                for newlink in linksNormal:
                    url=newlink.url
                    self.saveUrl(url, isNeedUpdateUrldump=False, isNeedSavetoDb=True, referenceUrl=response.url, priority=v['priority'])
           
            #item页link
            itemCounter = 0
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
                itemCounter += len(links)
                for link in links:
                    match=re.search(v['itemTidRegex'], link.url, 0)
                    if match and match.group(1):
                        tid=match.group(1)
                        newUrl=v['itemPrintPageFormat'] % tid
                        self.saveUrl(url, isNeedUpdateUrldump=False, isNeedSavetoDb=True, referenceUrl=response.url, priority=v['priority'])
                        log.msg("拼凑item打印链接：%s" %newUrl, level=log.DEBUG)
                    else:
                        log.msg("抽出的link:%s 没有发现tid，不能拼凑出新链接。请检查正则是否有误： linkXpath：%s、tid正则:%s" %(link.url,v['regex'],v['itemTidRegex']), level=log.ERROR)
            #item
            items = self.parseItem(response)
            if items and len(items)>0:
                log.msg('得到items，数量：%s'% len(items),level=log.DEBUG)
                reqs.extend(items)
            log.msg('抽出的列表页url数量:%s,抽出item页url数量：%s .url:%s' % (counterNor, itemCounter,response.url),level = log.INFO)
        #计数下载次数
        self.pendingRequestCounter -= 1
        #补充request
        if self.keepCrawlingSwitch and self.pendingRequestCounter <= 0:
            pendingRequest = self.getPendingRequest()
            reqs.extend(pendingRequest)
        return reqs
    
SPIDER = BaseBBSSpider2()