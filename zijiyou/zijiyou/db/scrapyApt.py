# coding:utf-8
'''
Created on 2011-9-21

@author: shiym
'''
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from scrapy.http.request import Request
from zijiyou.db.apt import mongoApt
import datetime

class SchedulerApt(object):
    '''
    scrapy调度数据层适配器
    '''
    
    def __init__(self):
        self.urlDbnamekey=settings.get('DB_URL')
        self.urlCollectionsMap=settings.get('DB_URL_COLLECTIONS_MAP')
        #pengdingRequest长度限制
        self.urlIncreasement=settings.get('MAX_INII_REQUESTS_SIZE')
        
    def makeRequest(self, url, referenceUrl=None,callBackFunctionName=None,meta={},urlId=None,priority=1, **kw): 
        '''
        创建Request
        '''
        if not urlId:
            raise NotConfigured('爬虫%s创建Request的url%s没有提供id，将导致无法更新url的状态' % (self.name,url))
        if(callBackFunctionName != None):
            print '危险：在scrapyApt初始化的request，只有函数名'
            kw.setdefault('callback', callBackFunctionName)
        meta['urlId']=urlId
        meta['download_timeout']=180
        meta['depth']=0
        kw.setdefault('meta',meta)
        kw.setdefault('priority',priority)
        return Request(url, **kw)
    
    def getRequestsToSupplyPendingreqeust(self,spiderName):
        """
        从数据库加载新url，创建request，补充pengdingRequest
        """
        whereJson={"status":1000}
        cursor=mongoApt.find(self.urlDbnamekey, self.urlCollectionsMap[spiderName], whereJson=whereJson, sortField='priority',limitNum=self.urlIncreasement)
        requests=[] 
        for p in cursor:
            req = self.makeRequest(p["url"], callBackFunctionName=p["callBack"], urlId=p['_id'],priority=p["priority"])
            requests.append(req)
            if len(requests)>=self.urlIncreasement:
                break
        return requests
    
    def getRequestWithUpdateStrategy(self,spiderName):
        """
        更新策略
        """
        whereJson={"status":{"$lt":400},"spiderName":spiderName,'updateInterval':{'$exists':True}}
        cursor =  mongoApt.find(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson, sortField='status')
        requests=[] 
        for p in cursor:
            if 'updateInterval' in p and p['status'] in [200, 304] and datetime.datetime.now()-datetime.timedelta(days=p["updateInterval"]) > p["dateTime"]:
                meta={}
                headers={}
                if 'reference' in p :
                    meta['reference'] = p['reference']
                if self.updateStrategy in p:
                    meta[self.updateStrategy]=p[self.updateStrategy]
                    headers['If-Modified-Since'] = self.getGMTFormatDate(p['dateTime'])
                req=self.makeRequest(p["url"], callBackFunctionName=p["callBack"],meta=meta, urlId=p['_id'],priority=p["priority"],headers=headers)
                requests.append(req)
        return requests
            
            
            