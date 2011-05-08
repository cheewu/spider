# -*- coding: utf-8 -*-
'''
Created on 2011-4-20

@author: shiym
'''
from bson.objectid import ObjectId
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from zijiyou.db.mongoDbApt import MongoDbApt
from zijiyou.spiders.offlineCrawl.extractorConfig import extractorConfig
from zijiyou.items.enumModel import LogLevel

import re
import datetime
import os

class Parse(object):
    '''
    模拟爬虫解析
    '''

    def __init__(self):
        '''
        Constructor
        '''
        logFileName=settings.get('OFFLINE_PARSE_LOG','/data/configs/offlineParseLog.log')
        if os.path.exists(logFileName):
            self.loger=open(logFileName,'a')
        else:
            self.loger=open(logFileName,'w+')
        self.parseLog( '开始解析程序，初始化。' , level=LogLevel.INFO)
        self.mon=MongoDbApt()
        self.colName="ResponseBody"
        self.requiredField= ['name','content']
        whereJson={'status':100}
#        self.responseBodys=self.mon.findByDictionaryAndSort(self.colName, whereJson)
        self.responseBodys=[]
        self.responseBodys.append(self.mon.findOne(self.colName))#test
        self.parseLog( 'length of response:%s' % len(self.responseBodys), level=LogLevel.INFO)
    
    def parse(self):
        if not self.responseBodys or len(self.responseBodys)<1:
            self.parseLog( '加载ResponseBody数为0!', level=LogLevel.WARNING)
            return
        
        heard={'Content-type':'text/html',
               'encoding':'utf-8',
               'Content-Type': ['text/html;charset=UTF-8'],
               'Pragma': ['no-cache'], 
               'Cache-Control': ['no-cache,no-store,must-revalidate']
               }
        items={}
        for p in self.responseBodys:
#            print p
            if not ('spiderName' in p and 'type' in p):
                self.parseLog( '缺失spiderName 或 type. Url:%s' % (p['pageUrl']), level=LogLevel.ERROR)
            spiderName=p['spiderName']
            itemType=re.sub('[\r\n]', "", p['type'])
            response=HtmlResponse(str(p['pageUrl']), status=200, headers=heard, body=str(p['content']), flags=None, request=None )
            item = self.parseItem(extractorConfig[spiderName],itemType, response)
            whereJson={'_id':ObjectId(p['_id'])}
            if item:
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
                
        self.parseLog('解析成功items数：%s' % len(items), level=LogLevel.INFO)
        if items and len(items)>0:
#            print items
            for k,v in items.items():
                
#                print v
#                print '++++++++++++++++++++++++++'
#                for p1,p2 in v[0].items():
#                    print 'key:%s,value:%s' % (p1,p2)
                
                if len(v)<1:
                    continue
                objId = self.mon.saveItem(k, v)
                if objId:
                    self.parseLog('item保存成功,collectionsName:%s, objectId:%s' % (k,objId), level=LogLevel.INFO)
                else:
#                    print v
                    self.parseLog('item保存失败！,collectionsName:%s ' % (k), level=LogLevel.ERROR)
        
        #关闭日志
        self.parseLog('解析出的items全部保存成功', level=LogLevel.INFO)
        self.loger.close()
        print 'OK'
        
    def parseItem(self,config, itemType, response):
        '''
        parse the page, get the information of attraction to initiate noteItem, then return items to pipeLine
        the pipeLine configured by "settings" will store the data
        '''
        hxs=HtmlXPathSelector(response)
        
        #define xpath rule
        if not itemType in config:
            self.parseLog('类型没有找到：%s ' % itemType, level=LogLevel.ERROR)
            raise NotConfigured
        item={}
        item['itemType']=itemType
        item['pageUrl']=response.url
        xpathItem = config[itemType]
        for k,v in xpathItem.items():
            values = hxs.select(v).extract()
            if not values or len(values)<1:
                self.parseLog('字段%s 为空 url：%s' %(k,response.url) ,level=LogLevel.WARNING)
                continue
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
            if not value and k in self.requiredField:
                self.parseLog('非item页，因为缺失属性：%s，类型： %s， url:%s' % (k,itemType,response.url), level=LogLevel.WARNING)                
                return None
            item[k]=value
            
        #用正则表达式
        regexItem={}
        regexName=itemType+'Regex'
        if regexName in config:
            regexItem=config[regexName]
        for k,v in regexItem.items():
            if k.endswith('Regex'):
                continue
            regex=k+'Regex'
            if not regex in regexItem:
                self.parseLog('找不到匹配的正则表达式，配置文件的%s配置缺少相应的%s' %(k,regex) ,level=LogLevel.WARNING)
                continue
            else:
                regex=regexItem[regex]
            values=hxs.select(v).re(regex)
            if not values or len(values)<1:
                self.parseLog('字段为空:%s  url：%s' %(k,response.url) ,level=LogLevel.WARNING)
                continue
            value=value=("-".join("%s" % p for p in values)).encode("utf-8")
            
            '''有些属性是必选的，有些属性是可选的，若必选的属性未抽取到，则说明该页面不是item页，直接返回None，若是可选的，则在判断条件中加入可选的属性进行过滤，如：attractions，feature'''
            if not value and k in self.requiredField:
                self.parseLog('非item页，因为缺失属性：%s，类型： %s， url:%s' % (k,itemType,response.url), level=LogLevel.WARNING)                
                return None
            item[k]=value
        self.parseLog('成功解析出一个item，类型：%s' % itemType, level=LogLevel.INFO)     
        return item
    
    def parseLog(self,msg,level=None):
        if not msg or not level or len(msg)<2:
            return
        self.loger.write('%s level=%s  :%s \n' %(datetime.datetime.now(),level,msg))
        
    def ExtText(self,input):
        pass

