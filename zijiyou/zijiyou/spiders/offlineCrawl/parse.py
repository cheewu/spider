# -*- coding: utf-8 -*-
'''
Created on 2011-4-20

@author: shiym
'''
from bson.objectid import ObjectId
from orca.braille import Region
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
from zijiyou.common import utilities
from zijiyou.config.extractorConfig import extractorConfig
from zijiyou.db.mongoDbApt import MongoDbApt
from zijiyou.items.enumModel import LogLevel
from zijiyou.items.zijiyouItem import UrlDb, PageDb, POI, Article, Note, \
    MemberInfo, MemberTrack, MemberFriend, MemberNoteList, KeyWord
from zijiyou.spiders.offlineCrawl.extractText import doExtract
import datetime
import json
import os
import re
import string


class Parse(object):
    '''
    模拟爬虫解析网页
    '''

    def __init__(self,isOffline=False):
        '''
        Constructor
        '''
        #离线爬虫初始化
        self.isOffline=isOffline
        if self.isOffline:   
            #需要单独的日志记录
            logFileName=settings.get('OFFLINE_PARSE_LOG')
            if os.path.exists(logFileName):
                self.loger=open(logFileName,'a')
            else:
                self.loger=open(logFileName,'w')
            #加载离线爬虫配置信息
            self.ResponseDb=settings.get('RESPONSE_DB')
            if not self.ResponseDb :
                self.parseLog('没有配置CRAWL_DB！，请检查settings', level=LogLevel.ERROR)
                raise NotConfigured
            self.mongoApt=MongoDbApt()
                
        self.parseLog( '开始解析程序，初始化。' , level=LogLevel.INFO)
        
        self.requiredField= ['name','content','title']
        self.specialField=['center','area','content','noteType']#,'content'
        self.specialItem=['MemberTrack']
        self.needMd5=['Article','Note']
        self.collectionNameMap={'Attraction':'POI',
                                 'Hotel':'POI'}
        self.whereJson={'status':100}#{'status':100} 测试
        self.limitNum=50
        self.responseTotalNum=0#self.mongoApt.countByWhere(self.ResponseDb, self.whereJson)
#        self.responseBodys=self.mongoApt.findFieldsWithLimit(self.ResponseDb, self.whereJson, self.limitNum)
        self.curSeek=0
#        self.parseLog( '初始length of response:%s，总长度：%s' % (self.curSeek,self.responseTotalNum), level=LogLevel.INFO)
#        print 'init完成'
    
    def parse(self):
        '''
        离线爬虫入口
        '''
        if self.responseTotalNum<1:
            self.responseTotalNum=self.mongoApt.countByWhere(self.ResponseDb, self.whereJson)
            self.responseBodys=self.mongoApt.findFieldsWithLimit(self.ResponseDb, self.whereJson, self.limitNum)
        
        heard={'Content-type':'text/html',
               'encoding':'utf-8',
               'Content-Type': ['text/html;charset=UTF-8'],
               'Pragma': ['no-cache'], 
               'Cache-Control': ['no-cache,no-store,must-revalidate']
               }
        self.countSuc=0;
        self.countFail=0
        def _parse():
            items={}
            for p in self.responseBodys:
                if not ('spiderName' in p and 'itemCollectionName' in p):
                    self.parseLog( '缺失spiderName 或 itemCollectionName. Url:%s' % (p['url']), level=LogLevel.ERROR)
                    continue
                spiderName=p['spiderName']
                itemCollectionName=re.sub('[\r\n]', "", p['itemCollectionName'])
                item = None
                if itemCollectionName in self.specialItem:
                    item = self.parseSpecialItem(itemCollectionName, p)
                else:
                    response=HtmlResponse(str(p['url']), status=200, headers=heard, body=str(p['responseBody']), flags=None, request=None )
                    item = self.parseItem(spiderName,itemCollectionName, response)
                whereJson={'_id':ObjectId(p['_id'])}
                if itemCollectionName in self.collectionNameMap:
                    itemCollectionName=self.collectionNameMap[itemCollectionName]
                if item:
                    if not itemCollectionName in items:
                        items[itemCollectionName]=[]
                    items[itemCollectionName].append(item)
                    # parse item successful, and then update the status to 200
                    updateJson={'status':200}
                    self.mongoApt.updateItem(self.ResponseDb, whereJson, updateJson)
                    self.countSuc+=1
                else:
                    # fail in parsing item , and then update the status to 101
                    updateJson={'status':101}
                    self.mongoApt.updateItem(self.ResponseDb, whereJson, updateJson)
                    self.countFail+=1
                    
            if items and len(items)>0:
                for k,v in items.items():
                    if len(v)<1:
                        continue
                    else:
                        print '新item的数量：%s，类型：%s' % (len(v),k)
                    objId = self.mongoApt.saveItem(k, v)
                    print '保存新item：%s, objId:%s' % (itemCollectionName,objId)
                    if objId:
                        self.parseLog('item保存成功,collectionsName:%s, objectId:%s' % (k,objId), level=LogLevel.INFO)
                    else:
                        self.parseLog('item保存失败！,collectionsName:%s ' % (k), level=LogLevel.ERROR)
                items = {}
            
        #非递归parse
        while (self.curSeek < self.responseTotalNum):
            self.parseLog('成功完成一轮递归，curSeek:%s' % self.curSeek, level=LogLevel.INFO)
            self.responseBodys=self.mongoApt.findFieldsWithLimit(self.ResponseDb, self.whereJson, self.limitNum)
            self.curSeek+=len(self.responseBodys)
            _parse()
        self.parseLog('解析完成，解析成功items数：%s 失败数量：%s' % (self.countSuc,self.countFail), level=LogLevel.INFO)
        
        #离线爬虫关闭日志
        self.parseLog('parse 完成', level=LogLevel.INFO)
        self.loger.close()
        if not self.loger.closed :
            self.loger.close()
            print 'OK !关闭日志'

    def parseItem(self,spiderName=None, itemCollectionName=None, response=None):
        '''
        parse the page, get the information of attraction to initiate noteItem, then return items to pipeLine
        the pipeLine configured by "settings" will store the data
        '''
        config=extractorConfig[spiderName]
        if not config:
            self.parseLog('解析配置信息没有找到，请检查extracotrConfig是否有爬虫%s的配置！ ' % spiderName, level=LogLevel.ERROR)
            raise NotConfigured
        hxs=HtmlXPathSelector(response)
        
        #define xpath rule
        if not itemCollectionName or not itemCollectionName in config:
            self.parseLog('类型没有找到：%s ' % itemCollectionName, level=LogLevel.ERROR)
            raise NotConfigured
        
        #耦合较大且代码重复，后续计划用工厂模式取代
        item=None
        if itemCollectionName == 'UrlDb':
            item=UrlDb()
        elif itemCollectionName == 'PageDb':
            item=PageDb()
        elif itemCollectionName == 'POI':
            item=POI()
        elif itemCollectionName == 'Article':
            item=Article()
        elif itemCollectionName == 'Note':
            item=Note()
        elif itemCollectionName == 'MemberInfo':
            item=MemberInfo()
        elif itemCollectionName == 'MemberTrack':
            item=MemberTrack()
        elif itemCollectionName == 'MemberFriend':
            item=MemberFriend()
        elif itemCollectionName == 'MemberNoteList':
            item=MemberNoteList()
        elif itemCollectionName == 'Region':
            item=Region()
        elif itemCollectionName == 'KeyWord':
            item=KeyWord()
        else:
            raise NotConfigured
        
        item['collectionName']=itemCollectionName
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
            if k in self.specialField:
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
            if k in self.specialField:
                value=self.parseSpecialField(k, value)
            item[k]=value
            
        #解析response中的数据
        respItem={}
        respName=itemCollectionName+'Resp'
        if respName in config:
            respItem=config[respName]
        for k,v in respItem.items():
            value = None
            if v == 'url':
                value = response.url
            elif v == 'header':
                if v.items():
                    header = response.headers
                    for hk, hv in v.items():
                        value = header[hv]
                        if not value:
                            self.parseLog('response.headers中没有该属性：%s，类型： %s' % (hk,itemCollectionName), level=LogLevel.WARNING)
                            continue
                        if not value and hk in self.requiredField:
                            self.parseLog('非item页，因为缺失属性：%s，类型： %s， url:%s' % (hk,itemCollectionName,response.url), level=LogLevel.WARNING)                
                            return None
                        if hk in self.specialField:
                            value=self.parseSpecialField(hk, value)
                        item[hk]=value
                    continue
                value = response.headers
            elif k == 'status':
                value = response.status
            
            if not value and k in self.requiredField:
                self.parseLog('非item页，因为缺失属性：%s，类型： %s， url:%s' % (k,itemCollectionName,response.url), level=LogLevel.WARNING)                
                return None
            if k in self.specialField:
                value=self.parseSpecialField(k, value)
            item[k]=value
            
        if itemCollectionName in self.needMd5:
            item['md5']=utilities.getFingerPrint(response.url, isUrl=True)
        
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
            #print mainText
            return mainText
        if name == 'noteType':
            noteTypeRegex = r':([^:]*)\.html'
            matches = re.search(noteTypeRegex,content,0)
            if matches:
                newContent = matches.group(1)
                return newContent
            
        return content
    
    def parseSpecialItem(self, itemCollectionName, pageItem):
        '''
        特殊Item解析
        '''
        self.parseLog('解析special item ：%s' % itemCollectionName, level=LogLevel.INFO)
        
        if not itemCollectionName or not pageItem or (not itemCollectionName in self.specialItem):
            return None
        item = {}
        item['url'] = pageItem['url']
        item['spiderName'] = pageItem['spiderName']
        responseBody = str(pageItem['responseBody'])
        if itemCollectionName == 'MemberTrack':
            if responseBody:
                bodyJson = json.loads(responseBody)
                if bodyJson and bodyJson['list1'] and len(bodyJson['list1']) > 0:
                    trackInfo = {'likeflag':[],
                                 'goneflag':[],
                                 'knowflag':[],
                                 'planflag':[]
                                 }
                    fieldMap = {'likeflag':'like',
                                'goneflag':'gone',
                                'knowflag':'know',
                                'planflag':'plan'
                                }
                    for value in bodyJson['list1']:
                        country = value['countryname']
                        region = value['regionname']
                        district = value['districtname']
                        track = country
                        #去掉名字重复的
                        if country != region:
                            track += "-" + region
                        if region != district:
                            track += "-" + district
                        for k,v in trackInfo.items():
                            #T代表有，F代表没有
                            if value[k] == 'T':
                                v.append(track)
                    
                    for k,v in fieldMap.items():
                        item[v] = trackInfo[k]
                        
#                    print item
        else:
            self.parseLog('%s 是一个specialItem，但是没被处理' % itemCollectionName, level=LogLevel.WARNING)
            return None
        
        return item
    
    def parseLog(self,msg,level=None):
        '''
        只解析离线爬虫
        '''
        if self.isOffline:
            if not msg or not level or len(msg)<2:
                return
            self.loger.write('%s level=%s  :%s \n' %(datetime.datetime.now(),level,msg))
        
    def ExtText(self,input):
        pass

#测试
#if __name__ == '__main__':
#    p=Parse()
#    p.parse()
#    print '解析完成了！'
