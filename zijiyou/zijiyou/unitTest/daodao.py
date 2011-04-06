# -*- coding: utf-8 -*-
'''
Created on 2011-3-28
中文
@author: shiym
'''
import re
from scrapy.contrib_exp.crawlspider import Rule
from scrapy.selector import HtmlXPathSelector

from zijiyou.items.zijiyouItem import ZijiyouItem
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
from zijiyou.items.itemLoader import ZijiyouItemLoader

class Daodao(BaseCrawlSpider):
    '''
    Spider for www.daodao.com
    '''
    name ="daodaoSpider1"
    # regexs
    regexHome=r'http://www.daodao.com/Lvyou$'           
    regexCountry=r'Tourism-g\d+-[a-z A-Z]+-Vacations.html$' # Tourism-g294232-Japan-Vacations.html
    regexArea=r'Attractions-g\d+-Activities-[a-z A-Z]+\.html$' # Attractions-g294232-Activities-Japan.html
    regexAreaList=r'Attractions-g\d+-Activities-oa\d+-[a-z A-Z]+\.html$'  # /Attractions-g294232-Activities-oa15-Japan.html
    regexAttraction=r'Attractions-g\d+-Activities-[a-z _ A-Z]+_[a-z _ A-Z]+\.html$' #    Attractions-g298115-Activities-Kanazawa_Ishikawa_Prefecture_Chubu.html
    regexAttractionList=r'Attractions-g\d+-Activities-oa\d+-[a-z _ A-Z]+_[a-z _ A-Z]+\.html$' #Attractions-g298115-Activities-oa15-Kanazawa_Ishikawa_Prefecture_Chubu.html
    
    homePage="http://www.daodao.com"
    allowed_domains = ["daodao.com"]
    start_urls = [
            'http://www.daodao.com/Lvyou'
            ]

    rules = [
            Rule(regexHome, 'parseHome'),
            Rule(regexCountry, 'parseCountry'),
            Rule(regexArea,'parseArea'),
            Rule(regexAreaList, 'parseAreaList'),
            Rule(regexAttraction, 'parseAttraction'),
            Rule(regexAttractionList, 'parseAttractionList')
            ]
    
    def parseNextPage(self,response,allowReg,pagePriority,**extra):
        '''
        get the links of nextPage , return the request
        '''
        print('****begin parseNextPage***********************************************************',pagePriority)
        reqs=[]
        links=self.extractLinks(response,allow=allowReg,**extra)
        #get the totalPangeNum
        totalPageNum=1
        startNum=15 #defaultValue
        testLoop=0
        if links!=[]:
            linkTemp=links[0].url
            firstPageUrl=re.sub('-oa\d+-', '%s' % '-', linkTemp, 1)
            firstPageRequest=self.makeRequest(firstPageUrl,priority=pagePriority)
            reqs.append(firstPageRequest)
            for i in range(0,totalPageNum): 
                url=re.sub('-oa\d+-', '-oa%d-' % (i*50+startNum), links[0].url, 1)
                req=self.makeRequest(url,priority=pagePriority)
                reqs.append(req)
            print('nextPageprint:%d' % pagePriority,reqs[0],reqs[-1])
            print('-----parseNextPage success----------------------------------------------------------loop=%d' % testLoop,pagePriority)
            if len(reqs)<1:
                print('$$$$$$ get no request:',allowReg)
            return reqs
        else:
            print('$$$$$ failed parseNextPage get links $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

    def parseHome(self,response):
        '''
        parse the homePage to get the country list 
        '''
        print('****begin parseHome***********************************************************')
        counter=0;
        reqs=[]
        
        hxs=HtmlXPathSelector(response);
        sites=hxs.select('//div[@class="box-t1 top-outer-loc"]')
        if sites !=[]:
            links=sites[0].select('.//ul/li/a/@href').extract()
            for link in links:
                counter+=1
                if counter<2 :
                    link=self.homePage+link
                    req=self.makeRequest(link,priority=self.priorityCounty)
                    reqs.append(req)
            print('parseHomeprint:',reqs)
            print('----------------homeParser get links =---------------------------',counter)
            return reqs            
        else:
            print('$$$$$$$$$$$$$$$$ failed parseHome get links =---------------------------',counter)
    
    def parseCountry(self,response):
        '''
        trave the countres receiving from parseHome, jump to the areaHome of each country
        '''
        print('***begin parseCountry*******************************************************')
        reqs=[]
        links=self.extractLinks(response,allow=self.regexArea,restrict_xpaths='//div[@class="mod-box-t1"]/ul/li')
        if links!=[]:
            link=links[0]
            req=self.makeRequest(link.url, priority=self.priorityArea)
            reqs.append(req)
            print('parseCountryprint:',req)
            print('----------------parseCountry success ----------------------------------------')
            return reqs
        else :
            print('$$$$$$$$$$$$$$$$ failed parseCountry get links $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        
    def parseArea(self,response):
        '''
        parse the areaHome to get the areaList request
        '''
        try:
            return self.parseNextPage(response, self.regexAreaList, self.priorityAreaList,restrict_xpaths='//div[@class="pagination"]/div[@class="pgLinks clearfix"]')
        except Exception:
            print("parseArea Exception:",Exception)
        
    def parseAreaList(self,response):
        '''
        parse the area list generated by parseArea to get the attractionsList request
        '''
        print('****begin parseAreaList***********************************************************')
        reqs=self.extractRequests(response, priority=self.priorityAttraction,allow=self.regexAttraction,restrict_xpaths='//div[@id="LOCATION_LIST"]')
        reqsTest=[len(reqs),'----',reqs[0]]
        print('parseAreaListprint:',reqs[0],reqs[-1])        
        print('-----parseAreaList success----------------------------------------------------------')
        return reqsTest
        
    def parseAttraction(self,response):
        '''
        parse AtractionsListHome to get the attractionsList request
        '''
        try:
            return self.parseNextPage(response, self.regexAttractionList, self.priorityAttractionList,restrict_xpaths='//div[@class="pagination"]/div[@class="pgLinks clearfix"]')
        except Exception:
            print ('parseAttration Exception:',Exception)           
        
    def parseAttractionList(self,response):
        '''
        trave the attractionsList, get the information of each attraction of the area directory, 
        rather then generate attractions request, jump into the attraction page using additional function named parseItem 
        '''
        print('****begin parseAttractionList to get item directory****************************************************')
        hxs=HtmlXPathSelector(response);
        sites=hxs.select('//div[@id="ATTRACTION_OVERVIEW"]/div[@class="attraction-list clearfix"]')
        
        items=[]
        print('**********items************************************************************')
        try:
            i=0
            for site in sites:
                i=0
                loader = ZijiyouItemLoader(ZijiyouItem(),response=response)
                names=site.select('.//div[@class="info"]/div[@class="title"]/a/text()').extract()
                name=("-".join("%s" % p for p in names)).encode("utf-8")
                if name:
                    loader.add_value('name', name)
                i+=1
                addresses=site.select('.//div[@class="info"]/address/span/text()').extract()
                address=("-".join("%s" % p for p in addresses)).encode("utf-8")
                if address:
                    loader.add_value('address',address)
                i+=1
                areas=site.select('.//div[@class="info"]/address/span[@class="country-name"]/text()').extract()
                area=("-".join("%s" % p for p in areas)).encode("utf-8")
                if area:
                    loader.add_value('area',area)
                i+=1
                tagss=site.select('.//div[@class="info"]/div[@class="typle"]/a/text()').extract()
                tags=("-".join("%s" % p for p in tagss)).encode("utf-8")
                if tags:
                    loader.add_value('tags', tags)
                i+=1
                item=loader.load_item()
                items.append(item)
        except KeyError:
            print KeyError
            print('$$$$exception$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ i=',i)
        print('XXXXXXXXXXX中文中文XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        return items
    
        '''
    def parseItem(self,response):
        trave the attractionsList, get the information of each attraction of the area directory, 
        rather then generate attractions request, jump into the attraction page using additional function named parseItem 
        
        print('****begin parseAttractionList to get item directory****************************************************')
        hxs=HtmlXPathSelector(response);
        sites=hxs.select('//div[@id="ATTRACTION_OVERVIEW"]/div[@class="attraction-list clearfix"]')
        items=[]
        print('**********items************************************************************')
        for site in sites:
            loader = zijiyouItemLoader(zijiyouItem(),response=response)
            loader.add_xpath('name', '')
            loader.add_xpath('area','')
            loader.add_value('tags','')
            loader.add_xpath('address','')
            loader.add_value('photos','')
            items.append(loader.item)
            print(item)
        print('XXXXXXXXXXX成成成XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        return items
        '''
SPIDER = Daodao()