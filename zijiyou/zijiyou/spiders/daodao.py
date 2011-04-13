# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy.contrib_exp.crawlspider import Rule
from scrapy.selector import HtmlXPathSelector
from zijiyou.items.itemLoader import ZijiyouItemLoader
from zijiyou.items.zijiyouItem import ZijiyouItem, ContentItem, NoteItem
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
import re
import scrapy.log
#from scrapy.conf import settings 


class Daodao(BaseCrawlSpider):
    '''
    Spider for www.daodao.com
    '''
    name ="daodaoSpider"
    # regexs
    regexHome=r'http://www.daodao.com/Lvyou.*'
    regexArea=r'Attractions-g\d+-Activities-.*\.html$'
    regexAttraction=r'Attractions-g\d+-Activities[-oa\d]?-?[a-z _ A-Z]+_[a-z _ A-Z]+\.html$'
    regexAttractionItem=r'Attraction_Review-g\d+-.*-Reviews-.*.html$'
    
    #Travel Notes
    regexNoteEntry=r'Tourism-g\d+-c0-.*\.html$'
    regexNote=r'Tourism-g\d+-c\d+-n\d+.*\.html$'
    regexNoteItem=r'Tourism-g\d+-c0-.*\.html$'
    
    #XPath
    xpathNextPage="//a[@class='next sprite-arrow-right-green ml6 ']/@href"
    
    homePage="http://www.daodao.com"
    allowed_domains = ["daodao.com"]
    start_urls = [
            'http://www.daodao.com/Lvyou'
            ]

    rules = [Rule(regexHome, 'parseHome')] # It's a evil that Managing callBack order depends on rules
    
    '''
    def __init__(self):        
        #scrapy.log.start(logfile=settings.get("LOG_FILE", "zijiyou.log"), loglevel=scrapy.log.INFO)
        print ('begin!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        scrapy.log.start(logfile="zijiyou.log", loglevel=scrapy.log.INFO)
    '''
            
    def parseNextPage(self,response,nextPageXPath,pagePriority,callBackFunction):
        '''
        get the links of nextPage , return the request
        '''
        #print('****begin parseNextPage***********************************************************',pagePriority)
        reqs=[]
        hxs=HtmlXPathSelector(response)
        links = hxs.select(nextPageXPath).extract()
        if links != []:
            link = links[0]
            link = self.homePage + link
            req = self.makeRequest(link,callBackFunction,priority=pagePriority) # request for the nextPage
            reqs.append(req)
        return reqs
    
    def parseHome(self,response):
        '''
        get requests of country
        default callBack is parseCountry
        '''
        #print('****begin parseHome***********************************************************')
        scrapy.log.start(logfile="zijiyou.log", loglevel=scrapy.log.INFO)
        reqs=[]
        
        hxs=HtmlXPathSelector(response);
        xpathHome=['//div[@class="box-t1 top-outer-loc"]',
                   './/ul/li/a/@href']
        sites=hxs.select(xpathHome[0]) # get two block, should be configured
        if sites !=[]:
            links=sites[0].select(xpathHome[1]).extract() # should be configured by a flag indicating ONLY
            for link in links:
                link=self.homePage+link
                req=self.makeRequest(link,self.parseCountry,priority=self.priorityCounty)
                reqs.append(req)
            if len(reqs)<1:
                self.log("Cann't find any links of the country under the block from:%s"% response.url,level=scrapy.log.ERROR)                
            #print('parseHomeprint:---------------------------------------------------------',len(reqs),reqs[0])
        else:
            self.log("Cann't find any block of the country",level=scrapy.log.ERROR)
        return reqs[0:1]
    
    def parseCountry(self,response):
        '''
        jump to the area. default callBack is parseArea
        '''
        print('***begin parseCountry*******************************************************')
        reqs=[]
        xpathCountry=['//div[@class="mod-box-t1"]/ul/li']
        areaLinks=self.extractLinks(response,allow=self.regexArea,restrict_xpaths=xpathCountry[0])
        if areaLinks!=[]:
            link=areaLinks[0]
            req=self.makeRequest(link.url,self.parseArea, priority=self.priorityArea)
            #reqs.append(req)
        else :
            self.log("Cann't find any links of the Area from:%s" % response.url,level=scrapy.log.ERROR)
        #print('parseCountry success:---------------------------------------------------------',len(reqs),reqs[0])
        # cann't crawl all the info directory
        '''process the note entry'''
        noteLinks=self.extractLinks(response,allow=self.regexNoteEntry,restrict_xpaths=xpathCountry[0])
        if noteLinks!=[]:
            link=noteLinks[0]
            print 'noteEntry link:', link.url
            req=self.makeRequest(link.url,self.parseNote, priority=self.priorityNoteEntry)
            reqs.append(req)
        else :
            self.log("Cann't find any links of the Note Entry from:%s" % response.url,level=scrapy.log.ERROR)
        
        
        return reqs
        '''
        length=len(reqs)
        if length>8:
            return reqs[0:9]
        else:
            return reqs
        '''
        
    def parseArea(self,response):
        '''
        get the request of AttractionList whose callBack is parseAttraction. 
        And get the request of NextPage for recursive action, so this request's callBack is parseArea        
        '''
        print('****begin parseArea***********************************************************')
        xpathArea=['//div[@id="LOCATION_LIST"]'
                   ]
        xpathNextPage='//div[@class="pagination"]/div[@class="pgLinks clearfix"]'
        reqs=[]
        reqs1=self.extractRequests(response, self.priorityAttraction,self.parseAttraction,allow=self.regexAttraction,restrict_xpaths=xpathArea[0])
        reqs.extend(reqs1)
        if len(reqs)<1:
            self.log("Can't find any links of attraction from :%s" % response.url , level=scrapy.log.ERROR)
        reqs2= self.parseNextPage(response, xpathNextPage, self.priorityArea,self.parseArea)
        if len(reqs2)<1:
            self.log("Can't find nextPage Request from :%s" % response.url , level=scrapy.log.WARNING)
        else:
            # 被禁，暂时查第一页
            reqs.extend(reqs2)
            #pass            
        #print('-----parseArea success----------------------------------------------------------',len(reqs),reqs[0])
        return reqs
    
    def parseAttraction(self,response):
        '''
        get the request of AttractionItem whose callBack is parseItem.
        And get the request of NextPage for recursive action, so this request's callBack is parseAttraction
        '''
        print('***begin parseAttraction*******************************************************')
        reqs=[]
        xpathAttraction=['//div[@class="attraction-list clearfix"]/div[@class="clearfix"]/div[@class="info"]/div[@class="title"]'
                         ]
        xpathNextPage='//div[@class="pagination"]/div[@class="pgLinks clearfix"]'
        reqs.extend(self.extractRequests(response, self.priorityAttractionItem,self.parseItem,allow=self.regexAttractionItem,restrict_xpaths=xpathAttraction[0]))
        if len(reqs)<1:
            #print("Can't find any links of attractionItem from :%s" % response.url)
            self.log("Can't find any links of attractionItem from :%s" % response.url , level=scrapy.log.ERROR)
        
        reqs2= self.parseNextPage(response, xpathNextPage, self.priorityAttraction,self.parseAttraction)
        if len(reqs2)<1:
            #print("Can't find nextPage Request from :%s" % response.url)
            self.log("Can't find nextPage Request from :%s" % response.url , level=scrapy.log.WARNING)
        else:
            # 被禁，暂时查第一页
            #pass
            reqs.extend(reqs2)
        #print('-----parseAttraction success----------------------------------------------------------',len(reqs),reqs[0])
        return reqs #test
    
    def parseItem(self,response):
        '''    
        parse the page, get the information of attraction to initiate zijiyouItem, then return items to pipeLine
        the pipeLine configured by "settings" will store the data
        '''
        print('****begin parseAttractionList to get item directory****************************************************')
       
        hxs=HtmlXPathSelector(response);
        
        '''zijiyouItem'''
        print 'create zijiyou loader and start to load zijiyouItem' 
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
        loader.add_value('type', 'attraction')
        loader.add_value('content', response.body_as_unicode())
        contentItem = loader.load_item()
        
        '''create item to store every Item'''
        item = []
        item.append(zijiyouItem)
        item.append(contentItem)
        #print item[0]
        return item
    
    def parseNote(self, response):
        print('****begin parseNote***********************************************************')
        xpathNote=['//div[@class="article-list"]'
                   ]
        xpathNextPage='//div[@class="pagination"]/div[@class="pgLinks clearfix"]'
        reqs=[]
        reqs1=self.extractRequests(response, self.priorityNote,self.parseNoteItem, allow=self.regexNote,restrict_xpaths=xpathNote[0])
        reqs.extend(reqs1)
        if len(reqs)<1:
            self.log("Can't find any links of note from :%s" % response.url , level=scrapy.log.ERROR)
        reqs2= self.parseNextPage(response, xpathNextPage, self.priorityNote, self.parseNote)
        if len(reqs2)<1:
            self.log("Can't find nextPage Request from :%s" % response.url , level=scrapy.log.WARNING)
        else:
            # 被禁，暂时查第一页
            reqs.extend(reqs2)
            #pass            
        #print('-----parseArea success----------------------------------------------------------',len(reqs),reqs[0])
        return reqs[0:1]
    
    def parseNoteItem(self, response):
        '''    
        parse the page, get the information of attraction to initiate noteItem, then return items to pipeLine
        the pipeLine configured by "settings" will store the data
        '''
        print('****begin parseNoteItem to get item directory****************************************************')
       
        hxs=HtmlXPathSelector(response)
        
        '''noteItem'''
        print 'create note loader and start to load noteItem' 
        loader = ZijiyouItemLoader(NoteItem(),response=response)
        #define xpath rule
        xpath = r'//div[@class="article-title borderBom"]/div/h1/text()'
        title = ("-".join("%s" % p for p in hxs.select(xpath).extract())).encode("utf-8")
        loader.add_value("title", title)
        
        xpath = r'//div[@class="article-content"]'
        content = ("-".join("%s" % p for p in hxs.select(xpath).extract())).encode("utf-8")
        loader.add_value("content", content)
        
        xpath = r'//div[@class="article-title borderBom"]/p/span/text()'
        date = hxs.select(xpath)[-1].extract()
        loader.add_value("date", date)
        
        xpath = r'//ul[@class="article-extra borderBom"]/li'
        results = hxs.select(xpath)
        for i in range(len(results)):
            if(i == 0):
                area = ("-".join("%s" % p for p in results[i].select(r'div/a/text()').extract())).encode("utf-8")
                loader.add_value("area", area)
            elif(i == 1):
                type = ("-".join("%s" % p for p in results[i].select(r'a/text()').extract())).encode("utf-8")
                loader.add_value("type", type)
            elif(i == 2):
                tags = results[i].select(r'div/a/text()').extract()
                tag = ("-".join("%s" % p for p in tags)).encode("utf-8")
                loader.add_value("tag", tag)
            
        loader.add_value('pageUrl', response.url)
        noteItem = loader.load_item()
        #print noteItem
        
        '''contentItem''' 
        print 'create content loader and start to load contentItem' 
        loader = ZijiyouItemLoader(ContentItem(),response=response)
        loader.add_value('pageUrl', response.url)
        loader.add_value('type', 'note')
        loader.add_value('content', response.body_as_unicode())
        contentItem = loader.load_item()
        
        '''create item to store every Item'''
        item = []
        item.append(noteItem)
        item.append(contentItem)
        #print item[0]
        return item
    

SPIDER = Daodao()