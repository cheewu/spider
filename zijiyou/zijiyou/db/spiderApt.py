# coding:utf-8
'''
Created on 2011-8-5

@author: shiym
'''
from pymongo.objectid import ObjectId
from scrapy.conf import settings
from zijiyou.db.apt import mongoApt
import datetime

class OnlineApt(object):
    '''
    在线爬虫的数据库适配器
    '''
    
    def __init__(self):
        '''
        初始化
        '''
        self.urlDbnamekey=settings.get('DB_URL')
        self.urlCollectionsMap=settings.get('DB_URL_COLLECTIONS_MAP')
        #pengdingRequest长度限制
        self.urlIncreasement=settings.get('MAX_INII_REQUESTS_SIZE')
    
    def findPendingUrlsByStatusAndSpiderName(self,spiderName,statusBegin=400,statusEnd=800):
        '''
        未被下载或下载失败的url，以便相应爬虫的恢复
        '''
        whereJson={"status":{"$gte":statusBegin,"$lt":statusEnd},"spiderName":spiderName}
        return mongoApt.find(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson,sortField='priority',limitNum=self.urlIncreasement * 5) #self.urlIncreasement * 20
    
    def findPendingUrls4JinghuaByStatusAndSpiderName(self,spiderName):
        '''
        精华游记url处理：不下载item只要url
        '''
        whereJson = {"status":{"$gte":300,"$lt":1001},"priority":1}
        return mongoApt.find(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson,sortField='priority',limitNum=self.urlIncreasement * 5) #self.urlIncreasement * 20

    def updateUrlDbStatusByUrl(self,url,spiderName,status=200):
        '''
        更新数据库访问状态
        '''
        whereJson={"url":url}
        updateJson={"status":status, "dateTime":datetime.datetime.now()}
        mongoApt.update(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson, updateJson=updateJson)
    
    def findUrlsForDupfilter(self,spiderName):
        '''
        加载用于排重的url的md5值
        '''
        whereJson={"status":{"$lt":400},"spiderName":spiderName}
        return mongoApt.find(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson, sortField='status')

    def saveNewUrl(self,spiderName,urlItem={}):
        '''
        保存
        '''
        return mongoApt.save(self.urlDbnamekey,self.urlCollectionsMap[spiderName], item=urlItem)
    
#    def getUncompelitedSeUrlNumber(self,spiderName):
#        '''
#        未完成的item和搜索引擎item页的总数
#        '''
#        whereJson = {"status":1000,"spiderName":'baseSeSpider'}
#        return mongoApt.countByWhere(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson)
    
#    def removeUncompelitedSeUrl(self,spiderName):
#        '''
#        删除未完成的item和搜索引擎item页
#        '''
#        whereJson = {"status":1000,"spiderName":'baseSeSpider'}
#        mongoApt.remove(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson)
    
    def getCompelitedSeListUrl(self,spiderName):
        '''
        已经完成的搜索引擎list页的总数
        '''
        whereJson = {"status":{"$lte":400},"spiderName":spiderName,"priority":{"$lt":999}}
        return mongoApt.countByWhere(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson)
    
    def removeCompelitedSeListUrl(self,spiderName):
        '''
        清除已经完成的搜索引擎list页
        '''
        whereJson = {"status":{"$lte":400},"spiderName":spiderName,"priority":{"$lt":999}}
        mongoApt.remove(self.urlDbnamekey,self.urlCollectionsMap[spiderName], whereJson=whereJson)
        
    def findKerwordsForSespider(self):
        '''
        加载Se爬虫的搜素关键字
        '''
        colName='keyword'
        return mongoApt.find(self.urlDbnamekey,colName)
    
class OfflineApt(object):
    '''
    离线爬虫apt
    '''
    
    def __init__(self):
        '''
        初始化
        '''
        self.dbItem=settings.get('DB_ITEM')
    
    def findUnparsedPageByStatus(self,spiderName):
        '''
        查询待解析的Page，通过状态
        '''
        colName='Page'
        whereJson={'status':{'$lt':200}}
#        whereJson={'_id':ObjectId('4e5a783c25e25797a2b90989')}
        cursor = mongoApt.find(spiderName,colName, whereJson=whereJson)
        return cursor
    
    def updatePageStatusAsSuccessById(self,pageId,spiderName):
        '''
        更新PageDb的状态为解析成功状态
        '''
        colName='Page'
        mongoApt.update(spiderName,colName, whereJson={'_id':ObjectId(pageId)}, updateJson={'status':200,'optDateTime':datetime.datetime.now()})
        
    def updatePageStatusAsUnsuccessById(self,pageId,spiderName):
        '''
        更新PageDb的状态为解析失败状态
        '''
        colName='Page'
        mongoApt.update(spiderName,colName, whereJson={'_id':ObjectId(pageId)}, updateJson={'status':101,'optDateTime':datetime.datetime.now()})
        
    def saveParsedItemToItemCollection(self,itemCollectionName,item):
        '''
        保存解析结果
        '''
        colName=itemCollectionName
        mongoApt.save(self.dbItem,colName, item)
        