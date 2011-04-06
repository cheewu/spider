#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from scrapy.contrib_exp.crawlspider import Rule
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector

from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
from scrapy.contrib_exp.crawlspider import CrawlSpider
from scrapy.conf import settings
import sys 
#sys.setdefaultencoding('utf-8')

reload(sys)

settings.overrides['DOWNLOAD_DELAY'] = 2

# global url set
UrlSet = set()
f = open("daodao/data/namelist.txt","w+")

def InitalUrlSet():
    f = open()

class NameListSpider(BaseCrawlSpider):
    '''
    Spider for www.daodao.com
    '''
    name ="nameListSpider"

    # regexs
    regexHomePage = r'http://www.daodao.com/Lvyou$'
    regexIndex = r'Attractions-.*-Activities-.*\.html$' #http://www.daodao.com/Attractions-g255055-Activities-Australia.html

                                                        #http://www.daodao.com/Tourism-g255055-Australia-Vacations.html

    allowed_domains = ["daodao.com"]
    start_urls = [
            'http://www.daodao.com/Lvyou'
            ]

    rules = [
            Rule(regexHomePage, 'parseHomePage'),            
            Rule(regexIndex, 'parseIndexPage')
            ]

    #URL not set 

    def parseHomePage(self,response):

        hxs = HtmlXPathSelector(response)

        links = hxs.select("//map[@name='Map']/area/@href").extract()
        links += hxs.select("//map[@name='Map2']/area/@href").extract()

        #print links
        reqs = []
        for link in links:
            list = link.split("-")
            link = "http://www.daodao.com/Attractions-" + list[1] + "-Activities-" + list[2] +".html"
            #print link
            if link not in UrlSet:
                req = self.makeRequest(link,priority=self.priority_area) # request for the linkListPage
                reqs.append(req)
                UrlSet.add(link)
        return reqs


    def parseIndexPage(self,response):

        hxs = HtmlXPathSelector(response)
        
        PalceNameList = hxs.select("//ul[@class='geoList']/li/a/text()").extract()
        if PalceNameList != []:
            for name in PalceNameList:
                #name = name.decode("ascii").encode("utf-8")
                name = name.encode("utf-8")
                f.write(name+"\n")
                #print name

        # get the next page link and add to the crawl list
        reqs = []
        linklist = hxs.select("//a[@class='next sprite-arrow-right-green ml6 ']/@href").extract()
        if linklist != []:
            link = linklist[0]    
            link = "http://www.daodao.com" + link
            #print link
            if link not in UrlSet:
                req = self.makeRequest(link,priority=self.priority_area) # request for the linkListPage
                reqs.append(req)
                UrlSet.add(link)
        return reqs


SPIDER = NameListSpider()


