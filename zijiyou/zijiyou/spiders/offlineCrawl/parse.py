# -*- coding: utf-8 -*-
'''
Created on 2011-4-20

@author: shiym
'''
from bson.objectid import ObjectId
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
from zijiyou.db.mongoDbApt import MongoDbApt
from zijiyou.spiders.offlineCrawl.extractorConfig import extractorConfig
import re

class Parse(object):
    '''
    模拟爬虫解析
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.mon=MongoDbApt()
        self.colName="ResponseBody"
        queJson={'status':100}
        self.responseBodys=self.mon.findByDictionaryAndSort(self.colName, queJson, None)
        print 'length of response:%s' % len(self.responseBodys)
    
    def parse(self):
        if not self.responseBodys or len(self.responseBodys)<1:
            print 'None response has been selected!'
            return
        
        heard={'Content-type':'text/html',
               'encoding':'utf-8',
               'Content-Type': ['text/html;charset=UTF-8'],
               'Pragma': ['no-cache'], 
               'Cache-Control': ['no-cache,no-store,must-revalidate']
               }
        items={}
        count=0;
        for p in self.responseBodys:
            if not ('spiderName' in p and 'type' in p):
                print '缺失spiderName 或 type. Url:%s' % p['pageUrl']
            spiderName=p['spiderName']
            itemType=re.sub('[\r\n]', "", p['type'])
            response=HtmlResponse(str(p['pageUrl']), status=200, headers=heard, body=str(p['content']), flags=None, request=None )
            print 'spiderName:%s, itemType:%s' %(spiderName,itemType)
            item = self.parseItem(extractorConfig[spiderName],itemType, response)
            whereJson={'_id':ObjectId(p['_id'])}
            if item:
                count+=1
                if not itemType in items:
                    items[itemType]=[]
                items[itemType].append(item)
                # parse item successful, and then update the status to 200
                updateJson={'status':200}
                self.mon.updateItem(self.colName, whereJson, updateJson)
            else:
                # fail in parsing item , and then update the status to 101
                updateJson={'status':101}
                self.mon.updateItem(self.colName, whereJson, updateJson)
                
        print '解析成功items数：%s' % count
        print items
        if items and len(items)>0:
            for k,v in items.items():
                if len(v)<1:
                    continue
                self.mon.saveItem(k, v)
        print '保存成功'
        
    def parseItem(self,config, itemType, response):
        '''
        parse the page, get the information of attraction to initiate noteItem, then return items to pipeLine
        the pipeLine configured by "settings" will store the data
        '''
        hxs=HtmlXPathSelector(response)
        
        #define xpath rule
        if not itemType in config:
            print '类型没有找到：%s ' % itemType
            raise NotConfigured
        xpathItem = config[itemType]
        item={}
        item['itemType']=itemType
        for k,v in xpathItem.items():
            values = hxs.select(v).extract()
            value=("-".join("%s" % p for p in values)).encode("utf-8")
            
            '''处理电话号码'''
            if(k == 'telNum'):
                if len(values) > 3:
                    value = re.search('\+\d+ [0-9 -]+', value, 0)
            '''处理回复数'''  
            if(k == 'replyNum'):
                value = re.search('\d+', value)
                if value:
                    value = value.group(0)
                else:
                    value = '0'
            '''有些属性是必选的，有些属性是可选的，若必选的属性未抽取到，则说明该页面不是item页，直接返回None，若是可选的，则在判断条件中加入可选的属性进行过滤，如：attractions，feature'''
            if not value and k in ['name','content']:
                print '%s:%s' %(k,value)
                print '非item页！:%s' %response.url                
                return None
            item[k]=value
        item['pageUrl']=response.url
        print item
                
        return item

