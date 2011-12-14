# -*- coding: utf-8 -*-
'''
Created on 2011-4-20

@author: shiym
'''
#from pymongo.objectid import ObjectId
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
from zijiyou.common.extractText import Extracter
from zijiyou.config.extractorConfig import extractorConfig
from zijiyou.db.spiderApt import OfflineApt
from zijiyou.items.enumModel import LogLevel
import datetime
import json
import os
import re
import string
import traceback

class Parse(object):
    '''
    模拟爬虫解析网页
    '''

    def __init__(self,isOffline=True):
        '''
        Constructor
        '''
        #正文抽取器
        self.ext = Extracter()
        #离线爬虫初始化
        self.isOffline=isOffline
        self.apt=OfflineApt()
        self.requiredField= ['content','title']
        self.specialField=['center','area','content','noteType']#,'content'
        self.specialItem=['MemberTrack']
        self.needMd5=['Article','Note']
        self.collectionNameMap=settings.get('COLLECTION_NAME_MAP')
        self.bbsSpiderName = settings.get('BBS_SPIDER_NAME')
        self.limitNum=50# test should be 50 
        self.responseTotalNum=0
        self.curSeek=0
        #是否需要列表格式的value。如imagelist需要的是list
        self.listFields = ['imageUrls'] 
    
    def parse(self,spiderName=[]):
        '''
        离线爬虫入口
        '''
        heard={'Content-type':'text/html',
               'encoding':'gb18030',
               'Content-Type': ['text/html;charset=gb18030'], #UTF-8
               'Pragma': ['no-cache'], 
               'Cache-Control': ['no-cache,no-store,must-revalidate']
               }
        spiderCodingMap={'55bbsSpider':'gb18030','daodaoSpider':'UTF-8',
                         'bbsSpider2':'gb18030',
                         'go2euSpider':'gb18030','lvpingSpider':'utf-8',
                         'lvyeSpider':'utf-8','sinabbsSpider':'gb18030'}
        self.countSuc = 0
        self.countFail = 0
        for sn in spiderName:
            #需要单独的日志记录
            if self.isOffline:   
                logFileName=settings.get('OFFLINE_PARSE_LOG')
                logFileName = logFileName + sn +'.log'
                if os.path.exists(logFileName):
                    self.loger=open(logFileName,'a')
                else:
                    self.loger=open(logFileName,'w')
            cursor=self.apt.findUnparsedPageByStatus(sn)
            #进度条
            numAll=cursor.count()
            thredHold = numAll / 100
            curNum = 0
            percents = 0.0
            print '开始解析%s...总数量：%s' % (sn,numAll)
            for p in cursor:
                #进度条
                curNum += 1
                if curNum >= thredHold:
                    curNum = 0
                    percents += 1.0
                    print '当前进度：百分之%s' % percents
                
                if not ('spiderName' in p and ('itemCollectionName' in p or p['spiderName'] in self.bbsSpiderName)):
                    self.parseLog('缺失spiderName 或 itemCollectionName. pageid:%s' % (p['_id']), level=LogLevel.ERROR)
                    continue
                spiderName = p['spiderName']
                itemCollectionName = ''
                if 'itemCollectionName' in p:
                    itemCollectionName = re.sub('[\r\n]', "", p['itemCollectionName'])
                else:
                    itemCollectionName='Article'
                item = None
                if itemCollectionName in self.specialItem:
                    item = self.parseSpecialItem(itemCollectionName, p)
                else:
                    if 'headers' in p:
                        heard = p['headers']
                    #对body进行编码
                    responseBody = p['responseBody']
                    if len(responseBody) <300 :
                        self.parseLog('responseBody为空或过少。id为%s，spidername=%s' % (p['_id'],p['spiderName']), level=LogLevel.WARNING)
                        continue
                    try:
                        if 'coding' in p:
                            if p['coding'] in ['windows-1252']:
                                responseBody = responseBody.decode('utf-8').encode('gb18030')
                            else:
                                responseBody = responseBody.decode('utf-8').encode(p['coding'])
                        else:
                            coding='utf-8'
                            if spiderName in spiderCodingMap:
                                coding=spiderCodingMap[spiderName]
                            responseBody = responseBody.decode('utf-8').encode(coding)
                        response = HtmlResponse(str(p['url']), status=200, headers=heard, body=str(responseBody).strip(), flags=None, request=None)
                        item = self.parseItem(spiderName, itemCollectionName, response, responseBody=str(p['responseBody']).strip(),pageid=p['_id'])
                    except Exception ,e:
                        self.parseLog('解析异常。id为%s的page编码为：%s，spidername=%s，异常信息：%s' % (p['_id'],p['coding'],p['spiderName'],str(e)), level=LogLevel.ERROR)
                        traceback.print_exc()
                        print '异常page的id：%s' % p['_id']
                        continue
                if itemCollectionName in self.collectionNameMap:
                    itemCollectionName = self.collectionNameMap[itemCollectionName]
                #成功解析出来item，保存item，更新pagedb状态为200
                if item:
                    self.apt.saveParsedItemToItemCollection(itemCollectionName, item)
                    self.apt.updatePageStatusAsSuccessById(p['_id'],sn)
                    self.countSuc += 1
                #没有成功解析item，pagedb更新为失败状态：101
                else:
                    self.apt.updatePageStatusAsUnsuccessById(p['_id'],sn)
                    self.countFail += 1

        self.parseLog('解析完成，解析成功items数：%s 失败数量：%s' % (self.countSuc,self.countFail), level=LogLevel.DEBUG)

        #离线爬虫关闭日志
        if self.loger and not self.loger.closed :
            self.loger.close()
            print 'OK !关闭日志'

    def parseItem(self,spiderName=None, itemCollectionName=None, response=None,responseBody='',pageid = ''):
        '''
        parse the page, get the information of attraction to initiate noteItem, then return items to pipeLine
        the pipeLine configured by "settings" will store the data
        '''
        #bbsSpider单独处理
        isbbsSpider = False
        if spiderName in self.bbsSpiderName:
            config = extractorConfig['BBsSpider']
            isbbsSpider = True
        else:
            config=extractorConfig[spiderName]
        if not config:
            raise NotConfigured('解析配置信息没有找到，请检查extracotrConfig是否有爬虫%s的配置！ ' % spiderName)
        
        hxs=HtmlXPathSelector(response)
        if not itemCollectionName or not itemCollectionName in config:
            raise NotConfigured('%s下载网页的类型%s没有找到，请检查解析配置文件' % (spiderName,itemCollectionName))
        
        item={};
        item['collectionName']=itemCollectionName
        if itemCollectionName in self.collectionNameMap:
            item['collectionName']=self.collectionNameMap[itemCollectionName]
        item['url']=response.url
        item['status']=100
        item['spiderName'] = spiderName
        xpathItem = config[itemCollectionName]
        #使用正文抽取，只要title、publishdate、content,imgList
        if 'mainext' in xpathItem and xpathItem['mainext']:
            title,publishdate,content,imgs = self.ext.doExtract(responseBody, threshold = config['threshold'] if 'threshold' in config else None,htmlId=pageid)
            if len(title) <1:
                self.parseLog('正文抽取未获得title，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
                return None
            if len(content) <10:
                self.parseLog('正文抽取未获得content，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
                return None
            if len(publishdate) < 1:
                self.parseLog('正文抽取未获得publishdate，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
            item['title'] = title
            item['publishDate'] = publishdate
            item['content'] = content
            item['images'] = imgs
            return item
        #xpath解析
        for k,v in xpathItem.items():
            value=''
            values = hxs.select(v).extract()
            if (not values or len(values)<1 or (" ".join("%s" % p for p in values)).strip() == "") and k in self.requiredField:
                self.parseLog('xpath解析发现item缺失属性：%s，类型： %s，spiderName:%s,xpath=%s, pageid:%s 。改用正文抽取尝试' % (k,itemCollectionName,spiderName,v,pageid), level=LogLevel.INFO)
                #若为Article，xpath没有解析出来，就用正文抽取再解析一次
                if item['collectionName'] == 'Article':
                    title,publishdate,content,imgs = self.ext.doExtract(responseBody, threshold = config['threshold'] if 'threshold' in config else None,htmlId=pageid)
                    if len(title) <1:
                        self.parseLog('正文抽取未获得title，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
                        return None
                    if len(content) <10:
                        self.parseLog('正文抽取未获得content，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
                        return None
                    if len(publishdate) < 1:
                        self.parseLog('正文抽取未获得publishdate，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
                    item['title'] = title
                    item['publishDate'] = publishdate
                    item['content'] = content
                    item['images'] = imgs
                    return item
            if k in self.listFields:
                item[k] = values
            else:
                value=("-".join("%s" % p for p in values)).encode("utf-8")
                if k in self.specialField:
                    value=self.parseSpecialField(k, value)
                if value :
                    item[k]=value.strip()
        #regex+xpath解析
        regexItem={}
        regexName=itemCollectionName+'Regex'
        if regexName in config:
            regexItem=config[regexName]
        for k,v in regexItem.items():
            if k.endswith('Regex'):
                continue
            regex=k+'Regex'
            if not regex in regexItem:
                raise NotConfigured('找不到匹配的正则表达式，配置文件的%s配置缺少相应的%s' %(k,regex))
            else:
                regex=regexItem[regex]
            values=hxs.select(v).re(regex)
            value=''
            #对bbs进行单独处理 @author 侯睿
            if isbbsSpider:
                value = values
                if k != 'content':
                    if type(values) == list:
                        value = value[0]
                elif type(value) == list:
                    filterWords = [
                        '标题:',
                        '作者:',
                        '时间:',
                        '标题：',
                        '作者：',
                        '时间：',
                    ]
                    filter = []
                    sig_p = 0
                    sig_start = 1
                    #过滤空字符
                    for p in value:
                        p_strip = p.strip()
                        if p_strip:
                            filter.append(p_strip)
                    value = filter
                    filter = []
                    #过滤空字符end
                    for p in value:
                        p_strip = p.strip()
                        if sig_p:
                            sig_p = 0
                            continue
                        if p_strip in filterWords:
                            if p_strip == '作者:':
                                if sig_start:
                                    sig_start = 0
                                else:
                                    filter.append("---------------------------------------------------------------------------------\n") 
                            sig_p = 1
                        #字数少于200被认为事无用的灌水回复
                        elif len(p_strip) > 200:
                            filter.append(p_strip+"\n")
                    value = (" ".join("%s" % p for p in filter)).encode("utf-8")
                    #删除掉一些垃圾。标题:.*[打印本页]   
                    if value:
                        value = re.sub('标题:.*\[打印本页\]', '', value)
                    if value.strip() == "" and k in self.requiredField:
                        self.parseLog('regex+xpath解析发现item缺失属性：%s，类型： %s，spiderName:%s, pageid:%s' % (k,itemCollectionName,spiderName,pageid), level=LogLevel.INFO)
                        return None
            #bbs单独处理end
            else:
                if (not values or len(values)<1 or (" ".join("%s" % p for p in values)).strip() == "") and k in self.requiredField:
                    self.parseLog('regex+xpath解析item缺失属性：%s，类型： %s，spiderName:%s, pageid:%s 。改用正文抽取尝试' % (k,itemCollectionName,spiderName,pageid), level=LogLevel.INFO)
                    #若为Article，xpath没有解析出来，就用正文抽取再解析一次
                    if item['collectionName'] == 'Article':
                        title,publishdate,content,imgs = self.ext.doExtract(responseBody, threshold = config['threshold'] if 'threshold' in config else None,htmlId=pageid)
                        if len(title) <1:
                            self.parseLog('正文抽取未获得title，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
                            return None
                        if len(content) <10:
                            self.parseLog('正文抽取未获得content，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
                            return None
                        if len(publishdate) < 1:
                            self.parseLog('正文抽取未获得publishdate，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
                        item['title'] = title
                        item['publishDate'] = publishdate
                        item['content'] = content
                        item['images'] = imgs
                        return item
                if len(values) == 1:
                    value=("-".join("%s" % p for p in values)).encode("utf-8")
                else:
                    value=values
                if k in self.specialField:
                    value=self.parseSpecialField(k, value)
            
            if value :
                item[k]=value.strip()
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
                            self.parseLog('非item页，因为缺失属性：%s，类型： %s， pageid:%s' % (hk,itemCollectionName,pageid), level=LogLevel.WARNING)                
                            #若为Article，xpath没有解析出来，就用正文抽取再解析一次
                            if item['collectionName'] == 'Article':
                                title,publishdate,content,imgs = self.ext.doExtract(responseBody, threshold = config['threshold'] if 'threshold' in config else None,htmlId=pageid)
                                if len(title) <1:
                                    self.parseLog('正文抽取未获得title，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
                                    return None
                                if len(content) <10:
                                    self.parseLog('正文抽取未获得content，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
                                    return None
                                if len(publishdate) < 1:
                                    self.parseLog('正文抽取未获得publishdate，spiderName:%s, pageid:%s' % (spiderName,pageid), level=LogLevel.WARNING)
                                item['title'] = title
                                item['publishDate'] = publishdate
                                item['content'] = content
                                item['images'] = imgs
                                return item
                        if hk in self.specialField:
                            value=self.parseSpecialField(hk, value)
                        item[hk]=value.strip()
                    continue
                value = response.headers
            elif k == 'status':
                value = response.status
            
            if not value and k in self.requiredField:
                self.parseLog('item缺失属性：%s，类型： %s，spiderName:%s, pageid:%s' % (k,itemCollectionName,spiderName,pageid), level=LogLevel.INFO)                
                return None
            elif not value:
                continue
            if k in self.specialField:
                value=self.parseSpecialField(k, value)
            item[k]=value.strip()
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
            if content == None or len(content)<100:
                return content
            mainText = self.ext.getText(content)
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
        self.parseLog('解析special item ：%s' % itemCollectionName, level=LogLevel.DEBUG)
        
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
                        
        else:
            self.parseLog('%s 是一个specialItem，但是没被处理' % pageItem['url'], level=LogLevel.WARNING)
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
        else:
            log.msg('%s level=%s  :%s \n' %(datetime.datetime.now(), level,msg))
        
    def ExtText(self,input):
        pass

##测试
#if __name__ == '__main__':
#    p=Parse(isOffline=True)
#    p.parse()
#    print '解析完成了！'
#    #初始排重
#    run(needCheckDup=True)
