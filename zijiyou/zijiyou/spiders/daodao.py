# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from scrapy.contrib_exp.crawlspider import Rule
from scrapy.selector import HtmlXPathSelector
from zijiyou.items.itemLoader import ZijiyouItemLoader
from zijiyou.items.zijiyouItem import ZijiyouItem, ContentItem, NoteItem
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
import re

class Daodao(BaseCrawlSpider):
    '''
    Spider for www.daodao.com
    '''
    functionDic={"parseNextPage":None,
                 "parseHome":None,
                 "parseCountry":None,
                 "parseArea":None,
                 "parseAttraction":None,
                 "parseItem":None,
                 "parseNote":None,
                 "parseNoteItem":None
                 }
    
    name ="daodaoSpider"
    # regexs
    regexHome=r'http://www.daodao.com/Lvyou.*'
    regexArea=r'Attractions-g\d+-Activities-.*\.html$'
    regexAttraction=r'Attractions-g\d+-Activities-.*\.html$'
    regexAttractionItem=r'Attraction_Review-g\d+-.*-Reviews-.*\.html$'
    
    #Travel Notes
    regexNoteEntry=r'Tourism-g\d+-c0-.*\.html$'
    regexNote=r'Tourism-g\d+-c\d+-n\d+.*\.html$'
    regexNoteItem=r'Tourism-g\d+-c0-.*\.html$'
    
    #XPath
    xpathNextPage="//div[@class='pgLinks clearfix']/a[@class='next sprite-arrow-right-green ']/@href"#"//a[@class='next sprite-arrow-right-green ml6 ']/@href" #next sprite-arrow-right-green 

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
        self.functionDic["parseNote"]=self.parseNote
        self.functionDic["parseNoteItem"]=self.parseNoteItem
        
        super(Daodao, self).__init__()
    
    def parseNextPage(self,response,nextPageXPath,pagePriority,callBackFunctionName):
        '''
        get the links of nextPage , return the request
        '''
        log.msg('****parseNextPage:%s' % response.url, loglevel=log.INFO)
        reqs=[]
        hxs=HtmlXPathSelector(response)
        links = hxs.select(nextPageXPath).extract()
        if links != []:
            link = links[0]
            link = self.homePage + link
            req = self.makeRequest(link,callBackFunctionName,priority=pagePriority) # request for the nextPage
            reqs.append(req)
            log.msg('****NextPage:%s' % link, loglevel=log.INFO)
        return reqs
    
    def parseHome(self,response):
        '''
        get requests of country
        default callBack is parseCountry
        '''
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
        else:
            log.msg("Cann't find any block of the country",level=log.ERROR)        
        log.msg('****parseHome numbers:%s***********************************************************' %len(reqs), loglevel=log.INFO)
        return reqs
    
    def parseCountry(self,response):
        '''
        jump to the area. default callBack is parseArea
        '''
        reqs=[]
        xpathCountry=['//div[@class="mod-box-t1"]/ul/li']
        '''process area'''
        areaLinks=self.extractLinks(response,allow=self.regexArea,restrict_xpaths=xpathCountry[0])
        if areaLinks!=[]:
            link=areaLinks[0]
            req=self.makeRequest(link.url,'parseArea', priority=self.priorityArea)
            reqs.append(req)
        else :
            log.msg("Cann't find any links of the Area from:%s" % response.url,level=log.ERROR)

        '''process the note entry'''
        noteLinks=self.extractLinks(response,allow=self.regexNoteEntry,restrict_xpaths=xpathCountry[0])
        if noteLinks!=[]:
            link=noteLinks[0]
            print 'noteEntry link:', link.url
            req=self.makeRequest(link.url,'parseNote', priority=self.priorityNoteEntry)
            reqs.append(req)
        else :
            self.log("Cann't find any links of the Note Entry from:%s" % response.url,level=log.ERROR)
        
        log.msg('****parseCountry numbers:%s**' %len(reqs), loglevel=log.INFO)
        return reqs
        
    def parseArea(self,response):
        '''
        areaList
        get the request of AttractionList whose callBack is parseAttraction. 
        And get the request of NextPage for recursive action, so this request's callBack is parseArea        
        '''
        xpathArea=['//div[@id="LOCATION_LIST"]'
                   ]
        reqs=[]
        
        reqs2= self.parseNextPage(response, self.xpathNextPage, self.priorityArea,"parseArea")
        if len(reqs2)<1:
            log.msg("Can't find nextPage Request from :%s" % response.url , level=log.WARNING)
        else:
            reqs.extend(reqs2)
            
        reqs1=self.extractRequests(response, self.priorityAttraction,"parseAttraction",allow=self.regexAttraction,restrict_xpaths=xpathArea[0])
        reqs.extend(reqs1)
        if len(reqs)<1:
            log.msg("Can't find any links of attraction from :%s" % response.url , level=log.ERROR)
                    
        log.msg('****parseArea numbers:%s**' %len(reqs), loglevel=log.INFO)        
        return reqs
    
    def parseAttraction(self,response):
        '''
        attractionList
        get the request of AttractionItem whose callBack is parseItem.
        And get the request of NextPage for recursive action, so this request's callBack is parseAttraction
        '''
        log.msg("****begin parseAttraction***********************************************************" ,level=log.INFO)
        reqs=[]        
        xpathAttraction=['//div[@class="attraction-list clearfix"]/div[@class="clearfix"]/div[@class="info"]/div[@class="title"]'
                         ]
        
        reqs2= self.parseNextPage(response, self.xpathNextPage, self.priorityAttraction,"parseAttraction")
        if len(reqs2)<1:
            log.msg("Can't find nextPage Request from :%s" % response.url , level=log.WARNING)
        else:
            reqs.extend(reqs2)
        
        reqs.extend(self.extractRequests(response, self.priorityAttractionItem,"parseItem",allow=self.regexAttractionItem,restrict_xpaths=xpathAttraction[0]))
        if len(reqs)<1:
            log.msg("Can't find any links of attractionItem from :%s" % response.url , level=log.ERROR)
        
        log.msg('****parseAttraction numbers:%s**' %len(reqs), loglevel=log.INFO)
        return reqs
    
    def parseItem(self,response):
        '''    
        parse the page, get the information of attraction to initiate zijiyouItem, then return items to pipeLine
        the pipeLine configured by "settings" will store the data
        '''
        log.msg("****parseItem froom:%s***" % response.url ,level=log.INFO)
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
        return item
    
    def parseNote(self, response):
        xpathNote=['//div[@class="article-list"]'
                   ]
        xpathNextPage='//div[@class="pagination"]/div[@class="pgLinks clearfix"]/a[@class="next sprite-arrow-right-green ml6"]/@href'
        reqs=[]
        
        reqs2= self.parseNextPage(response, xpathNextPage, self.priorityNote, 'parseNote')
        if len(reqs2)<1:
            self.log("Can't find nextPage Request from :%s" % response.url , level=log.WARNING)
        else:
            reqs.extend(reqs2)
            
        reqs1=self.extractRequests(response, self.priorityNote, 'parseNoteItem', allow=self.regexNote,restrict_xpaths=xpathNote[0])
        reqs.extend(reqs1)
        if len(reqs)<1:
            self.log("Can't find any links of note from :%s" % response.url , level=log.ERROR)
                    
        log.msg('****parseNote numbers:%s**' %len(reqs), loglevel=log.INFO)
        return reqs
    
    def parseNoteItem(self, response):
        '''    
        parse the page, get the information of attraction to initiate noteItem, then return items to pipeLine
        the pipeLine configured by "settings" will store the data
        '''
        log.msg('****begin parseNoteItem from:%s ********'% response.url, level=log.INFO)
       
        hxs=HtmlXPathSelector(response)
        
        '''noteItem'''
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
        
        '''contentItem''' 
        loader = ZijiyouItemLoader(ContentItem(),response=response)
        loader.add_value('pageUrl', response.url)
        loader.add_value('type', 'note')
        loader.add_value('content', response.body_as_unicode())
        contentItem = loader.load_item()
        
        '''create item to store every Item'''
        item = []
        item.append(noteItem)
        item.append(contentItem)
        return item
    
SPIDER = Daodao()
