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
#from zijiyou.spiders.offlineCrawl.ExtMainText import doExtMainText
from zijiyou.spiders.offlineCrawl.extractText import doExtract

import re
import datetime
import os
import string

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
            self.loger=open(logFileName,'w')
        self.parseLog( '开始解析程序，初始化。' , level=LogLevel.INFO)
        self.mongoApt=MongoDbApt()
        self.ResponseDb=settings.get('RESPONSE_DB')
        if not self.ResponseDb :
            self.parseLog('没有配置CRAWL_DB！，请检查settings', level=LogLevel.ERROR)
            raise NotConfigured
        self.requiredField= ['name','content','title']
        self.specailField=['center','area']#,'content'
        self.collectionNameMap={'Attraction':'POI',
                                 'Hotel':'POI'}
        self.whereJson={'status':100}#{'status':100} 测试
        self.limitNum=50
        self.responseTotalNum=self.mongoApt.countByWhere(self.ResponseDb, self.whereJson)
        self.responseBodys=self.mongoApt.findFieldsWithLimit(self.ResponseDb, self.whereJson, self.limitNum)
        self.curSeek=len(self.responseBodys)
        self.parseLog( '初始length of response:%s，总长度：%s' % (self.curSeek,self.responseTotalNum), level=LogLevel.INFO)
    
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
        countSuc=0;
        countFail=0
        for p in self.responseBodys:
            if not ('spiderName' in p and 'itemCollectionName' in p):
                self.parseLog( '缺失spiderName 或 itemCollectionName. Url:%s' % (p['url']), level=LogLevel.ERROR)
            spiderName=p['spiderName']
            itemCollectionName=re.sub('[\r\n]', "", p['itemCollectionName'])
            response=HtmlResponse(str(p['url']), status=200, headers=heard, body=str(p['responseBody']), flags=None, request=None )
            item = self.parseItem(extractorConfig[spiderName],itemCollectionName, response, spiderName)
            whereJson={'_id':ObjectId(p['_id'])}
            if itemCollectionName in self.collectionNameMap:
                #POI type
                item['type'] = itemCollectionName
                itemCollectionName=self.collectionNameMap[itemCollectionName]
            if item:
                if not itemCollectionName in items:
                    items[itemCollectionName]=[]
                items[itemCollectionName].append(item)
                # parse item successful, and then update the status to 200
                updateJson={'status':200}
                self.mongoApt.updateItem(self.ResponseDb, whereJson, updateJson)
                countSuc+=1
            else:
                # fail in parsing item , and then update the status to 101
                updateJson={'status':101}
                self.mongoApt.updateItem(self.ResponseDb, whereJson, updateJson)
                countFail+=1
                
        self.parseLog('解析完成，解析成功items数：%s 失败数量：%s' % (countSuc,countFail), level=LogLevel.INFO)
        if items and len(items)>0:
            for k,v in items.items():
                if len(v)<1:
                    continue
                objId = self.mongoApt.saveItem(k, v)
                print '保存新item：%s, objId:%s' % (itemCollectionName,objId)
                if objId:
                    self.parseLog('item保存成功,collectionsName:%s, objectId:%s' % (k,objId), level=LogLevel.INFO)
                else:
                    self.parseLog('item保存失败！,collectionsName:%s ' % (k), level=LogLevel.ERROR)
        
        #递归parse
        while (self.curSeek < self.responseTotalNum):
            self.parseLog('成功完成一轮递归，curSeek:%s' % self.curSeek, level=LogLevel.INFO)
            self.responseBodys=self.mongoApt.findFieldsWithLimit(self.ResponseDb, self.whereJson, self.limitNum)
            self.curSeek+=self.limitNum
            self.parse()
        
        #关闭日志
        self.parseLog('parse 完成', level=LogLevel.INFO)
        self.loger.close()
        if self.loger.closed :
            self.loger.close()
            print 'OK'

    def parseItem(self,config, itemCollectionName, response, spiderName=None):
        '''
        parse the page, get the information of attraction to initiate noteItem, then return items to pipeLine
        the pipeLine configured by "settings" will store the data
        '''
        hxs=HtmlXPathSelector(response)
        
        #define xpath rule
        if not itemCollectionName in config:
            self.parseLog('类型没有找到：%s ' % itemCollectionName, level=LogLevel.ERROR)
            raise NotConfigured
        item={}
        item['collectionName']=itemCollectionName
        print itemCollectionName
        if itemCollectionName in self.collectionNameMap:
            item['collectionName']=self.collectionNameMap[itemCollectionName]
#            print '切换类型：%s' % item['collectionName']
        item['url']=response.url
        item['status']=100
        item['spiderName'] = spiderName
        xpathItem = config[itemCollectionName]
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
                self.parseLog('非item页，因为缺失属性：%s，类型： %s， url:%s' % (k,itemCollectionName,response.url), level=LogLevel.WARNING)                
                return None
            if k in self.specailField:
                value=self.parseSpecialField(k, value)
            item[k]=value
        #用正则表达式
        regexItem={}
        regexName=itemCollectionName+'Regex'
        if regexName in config:
            regexItem=config[regexName]
        for k,v in regexItem.items():
            if k.endswith('Regex'):
                continue
            regex=k+'Regex'
            if not regex in regexItem:
                self.parseLog('找不到匹配的正则表达式，配置文件的%s配置缺少相应的%s' %(k,regex) ,level=LogLevel.ERROR)
                continue
            else:
                regex=regexItem[regex]
            values=hxs.select(v).re(regex)
            if not values or len(values)<1:
                self.parseLog('字段为空:%s  url：%s' %(k,response.url) ,level=LogLevel.WARNING)
                continue
            value=None
            if len(values) == 1:
                value=("-".join("%s" % p for p in values)).encode("utf-8")
            else:
                value=values
            if not value and k in self.requiredField:
                self.parseLog('非item页，因为缺失属性：%s，类型： %s， url:%s' % (k,itemCollectionName,response.url), level=LogLevel.WARNING)                
                return None
            if k in self.specailField:
                value=self.parseSpecialField(k, value)
            item[k]=value
        self.parseLog('成功解析出一个item，类型：%s' % itemCollectionName, level=LogLevel.INFO)
        return item
    
    def parseSpecialField(self,name,content):
        '''
        特殊处理的字段解析
        '''
        if not name or not content:
            return None
        if name == 'center':
            newContent=[]
            for i in range(0,len(content)):
                org=content[i]
                value=string.atof(org)
                newContent.append(value)
            return newContent 
        if name == 'area':
            if len(content.split('-'))<3:
                return content
            areaRegex=r'-(.*)-'
            matches=re.search(areaRegex,content,0)
            if matches:
                newContent = matches.group(1)
                return newContent
        if name == 'content':
            print '正文抽取'
            mainText = doExtract(content,threshold=False)
            print mainText
            return mainText
        
    def parseLog(self,msg,level=None):
        if not msg or not level or len(msg)<2:
            return
        self.loger.write('%s level=%s  :%s \n' %(datetime.datetime.now(),level,msg))
        
    def ExtText(self,input):
        pass

