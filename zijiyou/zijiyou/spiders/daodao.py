# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy.contrib_exp.crawlspider import Rule
from scrapy.selector import HtmlXPathSelector
from zijiyou.items.contentItem import ContentItem
from zijiyou.items.itemLoader import ZijiyouItemLoader
from zijiyou.items.zijiyouItem import ZijiyouItem
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
import re
from scrapy import log
#from scrapy.conf import settings 


class Daodao(BaseCrawlSpider):
    '''
    Spider for www.daodao.com
    '''
    functionDic={"parseNextPage":None,
                 "parseHome":None,
                 "parseCountry":None,
                 "parseArea":None,
                 "parseAttraction":None,
                 "parseItem":None
                 }
    
    name ="daodaoSpider"
    # regexs
    regexHome=r'http://www.daodao.com/Lvyou.*'
    regexArea=r'Attractions-g\d+-Activities-.*\.html$'
    regexAttraction=r'Attractions-g\d+-Activities[-oa\d]?-?[a-z _ A-Z]+_[a-z _ A-Z]+\.html$'
    regexAttractionItem=r'Attraction_Review-g\d+-.*-Reviews-.*.html$'
    #XPath
    xpathNextPage="//a[@class='next sprite-arrow-right-green ml6 ']/@href"
    
    homePage="http://www.daodao.com"
    allowed_domains = ["daodao.com"]
    start_urls = [
                  'http://www.daodao.com/Lvyou'
                  ]

    rules = [Rule(regexHome, 'parseHome')] # It's a evil that Managing callBack order depends on rules
    
    def __init__(self):
        '''
        initiate the functionDictionary
        '''
        log.msg("daodaoInit,initiate the functionDictionary", level=log.INFO)
        self.functionDic["parseNextPage"]=self.parseNextPage
        self.functionDic["parseHome"]=self.parseHome
        self.functionDic["parseCountry"]=self.parseCountry
        self.functionDic["parseArea"]=self.parseArea
        self.functionDic["parseAttraction"]=self.parseAttraction
        self.functionDic["parseItem"]=self.parseItem
        
        super(Daodao, self).__init__()
    
    def parseNextPage(self,response,nextPageXPath,pagePriority,callBackFunctionName):
        '''
        get the links of nextPage , return the request
        '''
        log.msg('****begin parseNextPage***********************************************************', loglevel=log.INFO)
        reqs=[]
        hxs=HtmlXPathSelector(response)
        links = hxs.select(nextPageXPath).extract()
        if links != []:
            link = links[0]
            link = self.homePage + link
            req = self.makeRequest(link,callBackFunctionName,priority=pagePriority) # request for the nextPage
            reqs.append(req)
        return reqs
    
    def parseHome(self,response):
        '''
        get requests of country
        default callBack is parseCountry
        '''
        log.msg('****begin parseHome***********************************************************', loglevel=log.INFO)
        reqs=[]
        
        hxs=HtmlXPathSelector(response);
        xpathHome=['//div[@class="box-t1 top-outer-loc"]',
                   './/ul/li/a/@href']
        sites=hxs.select(xpathHome[0]) # get two block, should be configured
        if sites !=[]:
            links=sites[0].select(xpathHome[1]).extract() # should be configured by a flag indicating ONLY
            for link in links:
                link=self.homePage+link
                req=self.makeRequest(link,"parseCountry",priority=self.priorityCounty)
                reqs.append(req)
            if len(reqs)<1:
                log.msg("Cann't find any links of the country under the block from:%s"% response.url,level=log.ERROR)                
            #print('parseHomeprint:---------------------------------------------------------',len(reqs),reqs[0])
        else:
            log.msg("Cann't find any block of the country",level=log.ERROR)
        return reqs[0:1]
    
    def parseCountry(self,response):
        '''
        jump to the area. default callBack is parseArea
        '''
        log.msg('***begin parseCountry*******************************************************', loglevel=log.INFO)
        reqs=[]
        xpathCountry=['//div[@class="mod-box-t1"]/ul/li']
        links=self.extractLinks(response,allow=self.regexArea,restrict_xpaths=xpathCountry[0])
        if links!=[]:
            link=links[0]
            req=self.makeRequest(link.url,"parseArea", priority=self.priorityArea)
            reqs.append(req)
        else :
            log.msg("Cann't find any links of the Area from:%s" % response.url,level=log.ERROR)
        # cann't crawl all the info directory
        return reqs[0:1]
        
    def parseArea(self,response):
        '''
        get the request of AttractionList whose callBack is parseAttraction. 
        And get the request of NextPage for recursive action, so this request's callBack is parseArea        
        '''
        log.msg("****begin parseArea***********************************************************" ,level=log.INFO)
        xpathArea=['//div[@id="LOCATION_LIST"]'
                   ]
        xpathNextPage='//div[@class="pagination"]/div[@class="pgLinks clearfix"]'
        reqs=[]
        reqs1=self.extractRequests(response, self.priorityAttraction,"parseAttraction",allow=self.regexAttraction,restrict_xpaths=xpathArea[0])
        reqs.extend(reqs1)
        if len(reqs)<1:
            log.msg("Can't find any links of attraction from :%s" % response.url , level=log.ERROR)
        reqs2= self.parseNextPage(response, xpathNextPage, self.priorityArea,"parseArea")
        if len(reqs2)<1:
            log.msg("Can't find nextPage Request from :%s" % response.url , level=log.WARNING)
        else:
            # 被禁，暂时查第一页
            #reqs.extend(reqs2)
            pass            
        #print('-----parseArea success----------------------------------------------------------',len(reqs),reqs[0])
        return reqs[0:1]
    
    def parseAttraction(self,response):
        '''
        get the request of AttractionItem whose callBack is parseItem.
        And get the request of NextPage for recursive action, so this request's callBack is parseAttraction
        '''
        log.msg("****begin parseAttraction***********************************************************" ,level=log.INFO)
        reqs=[]
        xpathAttraction=['//div[@class="attraction-list clearfix"]/div[@class="clearfix"]/div[@class="info"]/div[@class="title"]'
                         ]
        xpathNextPage='//div[@class="pagination"]/div[@class="pgLinks clearfix"]'
        reqs.extend(self.extractRequests(response, self.priorityAttractionItem,"parseItem",allow=self.regexAttractionItem,restrict_xpaths=xpathAttraction[0]))
        if len(reqs)<1:
            #print("Can't find any links of attractionItem from :%s" % response.url)
            log.msg("Can't find any links of attractionItem from :%s" % response.url , level=log.ERROR)
        
        reqs2= self.parseNextPage(response, xpathNextPage, self.priorityAttraction,"parseAttraction")
        if len(reqs2)<1:
            #print("Can't find nextPage Request from :%s" % response.url)
            log.msg("Can't find nextPage Request from :%s" % response.url , level=log.WARNING)
        else:
            # 被禁，暂时查第一页
            pass
            #reqs.extend(reqs2)
        #print('-----parseAttraction success----------------------------------------------------------',len(reqs),reqs[0])
        return reqs[0:1] #test
    
    def parseItem(self,response):
        '''    
        parse the page, get the information of attraction to initiate zijiyouItem, then return items to pipeLine
        the pipeLine configured by "settings" will store the data
        '''
        log.msg("****begin parseAttractionList to get item directory***********************************************************" ,level=log.INFO)
        hxs=HtmlXPathSelector(response);
        
        '''zijiyouItem'''
        loader = ZijiyouItemLoader(ZijiyouItem(),response=response)
        #define xpath rule
        xpathItem={r'name':r'//div[@class="wrpHeader clearfix"]/h1[@id="HEADING"]/text()',
                   r'area':r'//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li/a/text()',
                   r'address':r'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/span/text()',
                   r'desc':r'//div[@class="clearfix"]/div/div[@class="review-intro"]/p/text()',
                   r'descLink':r'//div[@class="clearfix"]/div/div[@class="review-intro"]',
                   r'popularity':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()',
                   r'telNum':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()'
        }
        
        for k,v in xpathItem.items():
            values = hxs.select(v).extract()
            value=("-".join("%s" % p for p in values)).encode("utf-8")
            if(k == 'telNum'):
                if len(values) > 3:
                    value = re.search('\+\d+ [0-9 -]+', value, 0)
                    if value:
                        #print ('telNum: %s' % telNum.group(0))
                        loader.add_value(k, value.group(0))
            else:
                if value:
                    loader.add_value(k, value)
        
        loader.add_value('pageUrl', response.url)
        zijiyouItem = loader.load_item()
        
        '''contentItem''' 
        print 'create content loader and start to load contentItem' 
        loader = ZijiyouItemLoader(ContentItem(),response=response)
        loader.add_value('pageUrl', response.url)
        loader.add_value('content', response.body_as_unicode())
        contentItem = loader.load_item()
        
        '''create item to store every Item'''
        item = []
        item.append(zijiyouItem)
        item.append(contentItem)
        #print item[0]
        return item

SPIDER = Daodao()