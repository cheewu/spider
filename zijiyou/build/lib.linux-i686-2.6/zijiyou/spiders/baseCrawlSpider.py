# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''

from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib_exp.crawlspider import CrawlSpider
from scrapy.conf import settings

class BaseCrawlSpider(CrawlSpider):
    '''
    base spider. to be inherited
    '''
    
    priorityCounty=10
    priorityArea = 100
    priorityAttraction = 200
    priorityAttractionItem=500

    def extractLinks(self, response, **extra): 
        """ 
        Extract links from response
        extra - passed to SgmlLinkExtractor
        """

        link_extractor = SgmlLinkExtractor(**extra)
        links = link_extractor.extract_links(response)
        return links

    def extractRequests(self, response, pagePriority,callBackFunction, **extra): 
        '''
        extract links identified by extra, then makeRequests 
        '''
        links = self.extractLinks(response, **extra)
        reqs = [self.makeRequest(link.url, callBackFunction,priority=pagePriority) for link in links]
        return reqs

    def makeRequest(self, url,callBackFunction, **kw): 
        '''
        make request
        '''
        kw.setdefault('callback', callBackFunction)
        req = Request(url, **kw)
        #req.meta['proxy'] = settings['PROXY']
        #print req.meta['proxy']
        return req