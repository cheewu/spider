# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
print '1111129'
class Daodao(BaseCrawlSpider):
    '''
    Spider for www.daodao.com
    '''
    name ="daodaoSpider"
            
    def myParse(self, response):
        '''start to parse response link'''
        print '解析link'
        log.msg('解析link', level=log.INFO)
        
        if not self.hasInit:
            self.initRequest()
            if self.pendingRequest and len(self.pendingRequest)>0:
                log.msg('从数据库查询的url开始crawl，len(pendingRequest)= %s' % len(self.pendingRequest), log.INFO)
                return self.pendingRequest
            
        log.msg('parse link: %s' % response.url, log.INFO)
        reqs = []
        '''普通页link'''
        for v in self.normalRegex:
            reqs.extend(self.extractRequests(response, v['priority'], allow = v['regex']))
           
        log.msg("%s parse 产生 普通页 url 数量：%s" % (response.url, len(reqs)), level=log.INFO)
 
        '''item页link'''
        for v in self.itemRegex:
            reqs.extend(self.extractRequests(response, v['priority'], allow = v['regex']))
            
        item = self.parseItem(response)
        if item:
            reqs.append(item)
        return reqs
    
SPIDER = Daodao()