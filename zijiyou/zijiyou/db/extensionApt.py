# coding:utf-8
'''
Created on 2011-8-5
爬虫扩展程序的数据库适配器
@author: shiym
'''
from scrapy.conf import settings
from zijiyou.db.apt import mongoApt

class DiagnoserApt(object):
    '''
    爬虫诊断器的db适配器
    '''
    
    def __init__(self):
        '''
        初始化
        '''
        self.urlDbnamekey=settings.get('DB_URL')
        self.urlCollectionsMap=settings.get('DB_URL_COLLECTIONS_MAP')
    
    def countErrorStatusUrls(self):
        '''
        总下载失败网页数量
        '''
        whereJson={'status':{'$gte':400,'$lt':900}}
        errorUrlNum=0
        for k in self.urlCollectionsMap.keys():
            errorUrlNum+=mongoApt.countByWhere(self.urlDbnamekey, k, whereJson=whereJson)
        return errorUrlNum
        
    def countUncrawlUrls(self):
        '''
        总剩余待爬取的网页数量
        '''
        whereJson={'status':{'$gt':900}}
        uncrawlNum=0
        for k in self.urlCollectionsMap.keys():
            uncrawlNum+=mongoApt.countByWhere(self.urlDbnamekey, k, whereJson=whereJson)
        return uncrawlNum
    
    def countItemsBySpidername(self,spiderName):
        '''
        爬虫诊断 计算指定爬虫已下载item页数量
        '''
        whereJson={'status':{'$gt':0}}
        colName='Page'
        itemNum=mongoApt.countByWhere(spiderName,colName, whereJson=whereJson)
        return itemNum
        
    def countUncrawlUrlsBySpidername(self,spiderName):
        '''
        爬虫诊断 计算指定爬虫待下载网页数量
        '''
        whereJson={'status':{'$gte':900}}
        uncrawlNum=mongoApt.countByWhere(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson)
        return uncrawlNum
        
    def countCrawledUrlsBySpidername(self,spiderName):
        '''
        爬虫诊断 计算指定爬虫已下载网页数量
        '''
        whereJson={'status':{'$lt':900,'$gt':0}}
        crawlNum=mongoApt.countByWhere(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson)
        return crawlNum
        
        