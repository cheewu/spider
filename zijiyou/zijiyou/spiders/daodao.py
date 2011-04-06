# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
import re
import scrapy.log
#from scrapy.conf import settings 
from scrapy.contrib_exp.crawlspider import Rule
from scrapy.selector import HtmlXPathSelector

from zijiyou.items.zijiyouItem import ZijiyouItem
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
from zijiyou.items.itemLoader import ZijiyouItemLoader

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
        return reqs[0:1] #test
    
    def parseCountry(self,response):
        '''
        jump to the area. default callBack is parseArea
        '''
        print('***begin parseCountry*******************************************************')
        reqs=[]
        xpathCountry=['//div[@class="mod-box-t1"]/ul/li']
        links=self.extractLinks(response,allow=self.regexArea,restrict_xpaths=xpathCountry[0])
        if links!=[]:
            link=links[0]
            req=self.makeRequest(link.url,self.parseArea, priority=self.priorityArea)
            reqs.append(req)
        else :
            self.log("Cann't find any links of the Area from:%s" % response.url,level=scrapy.log.ERROR)
        #print('parseCountry success:---------------------------------------------------------',len(reqs),reqs[0])
        # cann't crawl all the info directory
        return reqs[0:1]
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
            pass
            # 被禁，暂时查第一页
            #reqs.extend(reqs2)            
        #print('-----parseArea success----------------------------------------------------------',len(reqs),reqs[0])
        return reqs[0:1] 
    
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
            pass
            # 被禁，暂时查第一页
            #reqs.extend(reqs2)
        #print('-----parseAttraction success----------------------------------------------------------',len(reqs),reqs[0])
        return reqs #test
    
    def parseItem(self,response):
        '''    
        parse the page, get the information of attraction to initiate zijiyouItem, then return items to pipeLine
        the pipeLine configured by "settings" will store the data
        '''
        print('****begin parseAttractionList to get item directory****************************************************')
        
        loader = ZijiyouItemLoader(ZijiyouItem(),response=response)
        hxs=HtmlXPathSelector(response);
        
        names=hxs.select('//div[@class="wrpHeader clearfix"]/h1[@id="HEADING"]/text()').extract()
        name=("-".join("%s" % p for p in names)).encode("utf-8")
        if name:
            loader.add_value('name', name)
        addresses=hxs.select('//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/span/text()').extract()
        address=("-".join("%s" % p for p in addresses)).encode("utf-8")
        if address:
            loader.add_value('address',address)
        areas=hxs.select('//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li/a/text()').extract()
        area=("-".join("%s" % p for p in areas)).encode("utf-8")
        if area:
            loader.add_value('area',area)
        descs=hxs.select('//div[@class="clearfix"]/div/div[@class="review-intro"]/p/text()').extract()
        desc=("-".join("%s" % p for p in descs)).encode("utf-8")
        if desc:
            #print ('description:%s' % desc)
            loader.add_value('desc', desc)
        xpathLink='//div[@class="clearfix"]/div/div[@class="review-intro"]'
        descLink=self.extractLinks(response,restrict_xpaths=xpathLink)
        if descLink!=[]:
            #print ('descLink:%s' % descLink[0].url)
            loader.add_value('descLink', descLink[0].url)
        popularitys=hxs.select('//div[@class="leftContent"]/div[@class="ar-rank"]/span/strong/text()').extract()
        popularity=("-".join("%s" % p for p in popularitys)).encode("utf-8")
        if popularity:
            #print ('popularity: %s' % popularity)
            loader.add_value('popularity',popularity)
        telNums=hxs.select('//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()')
        if len(telNums)>3:
            telNum1=("-".join("%s" % p for p in telNums)).encode("utf-8")
            telNum=re.search('\+\d+ [0-9 -]+', telNum1, 0)
            if telNum:
                #print ('telNum: %s' % telNum.group(0))
                loader.add_value('telNum', telNum.group(0))
        loader.add_value('pageUrl', response.url)
        item=loader.load_item()
        return item
        
        '''
        loader = ZijiyouItemLoader(ZijiyouItem(),response=response)
        #homePath=r'//div[@class="clearfix"]/div/div[@class="hotel-info clearfix"]/div[@class="leftContent"]'
        print('+++++++++1')
        loader.add_xpath('name', '//div[@class="wrpHeader clearfix"]/h1[@id="HEADING"]/text()') 
        loader.add_xpath('area', '//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li/a/text()') 
        loader.add_xpath('address', '//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/span/text()') 
        print('+++++++++2')
        loader.add_xpath('desc', '//div[@class="clearfix"]/div/div[@class="review-intro"]/p/text()') 
        loader.add_xpath('popularity', '//div[@class="clearfix"]/div/div/div/div[@class="ar-rank"]/span/text()')
        loader.add_xpath('telNum', '//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/h3/text()') # 第3个 没有span标签
        loader.add_value('pageUrl', response.url)
        print('+++++++++3')
        item = loader.load_item()
        print(item)
        return item
        
        '''
        
        '''
        homePath=r'//div[@class="clearfix"]/div/div[@class="hotel-info clearfix"]/div[@class="leftContent"]'
        xpathItem={r'name':r'//div[@class="wrpHeader clearfix"]/h1[@id="HEADING"]/text()',
                   r'area':r'//div[@id="MAIN"]/div[class="crumbs"]/ul/li/ul/li/a/text()',
                   r'address':homePath+r'/div[@class="ar-detail"]/ul/li/span/text()',
                   r'desc':r'//div[@class="clearfix"]/div/div[@class="review-intro"]/text()',
                   r'popularity':homePath+r'/div[@class="ar-rank"]/span/text()',
                   r'telNum':homePath+r'/div[@class="ar-detail"]/ul/li/h3/text()'
        }
        itemAddValue={'pageUrl':response.url
                   }
        loader = ZijiyouItemLoader(ZijiyouItem(),response=response)
        print('+++++++++1',len(xpathItem.items()))
        for k,v in xpathItem.items():
            loader.add_xpath(k, v)
        print('+++++++++2')
        for k,v in itemAddValue.items():
            loader.add_value(k, v)
        item = loader.load_item()
        print('+++++++++3')
        print item #test
        return item
        '''

SPIDER = Daodao()