# coding:utf-8
'''
Created on 2011-8-5

@author: shiym
'''
from pymongo.objectid import ObjectId
from zijiyou.db.apt import mongoApt
import datetime

class OnlineApt(object):
    '''
    在线爬虫的数据库适配器
    '''
    
    def findPendingUrlsByStatusAndSpiderName(self,spiderName):
        '''
        未被下载或下载失败的url，以便相应爬虫的恢复
        '''
        colName='UrlDb'
        whereJson={"status":{"$gte":400},"spiderName":spiderName}
        return mongoApt.find(colName, whereJson=whereJson)

    def updateUrlDbStatusByUrl(self,url,status=200):
        '''
        更新数据库访问状态
        '''
        colName='UrlDb'
        whereJson={"url":url}
        updateJson={"status":status, "dateTime":datetime.datetime.now()}
        mongoApt.update(colName, whereJson=whereJson, updateJson=updateJson)
    
    def findUrlsForDupfilter(self,spiderName):
        '''
        加载用于排重的url的md5值
        '''
        colName='UrlDb'
        whereJson={"status":{"$lt":400},"spiderName":spiderName}
        return mongoApt.find(colName, whereJson=whereJson, sortField='status')

    def saveNewUrl(self,urlItem={}):
        '''
        保存
        '''
        colName='UrlDb'
        return mongoApt.saveItem(colName, item=urlItem)
    
    
    def getUncompelitedSeUrlNumber(self):
        '''
        未完成的item和搜索引擎list页的总数
        '''
        colName='UrlDb'
        whereJson = {"status":1000,"spiderName":'baseSeSpider'}
        return mongoApt.countByWhere(colName, whereJson=whereJson)
    
    def removeUncompelitedSeUrl(self):
        '''
        删除未完成的item和搜索引擎list页
        '''
        colName='UrlDb'
        whereJson = {"status":1000,"spiderName":'baseSeSpider'}
        mongoApt.remove(colName, whereJson=whereJson)
    
    def getCompelitedSeListUrl(self):
        '''
        已经完成的搜索引擎list页的总数
        '''
        colName='UrlDb'
        whereJson = {"status":{"lte":300},"spiderName":'baseSeSpider',"priority":{"$lt":1000}}
        return mongoApt.countByWhere(colName, whereJson=whereJson)
    
    def removeCompelitedSeListUrl(self):
        '''
        清除已经完成的搜索引擎list页
        '''
        colName='UrlDb'
        whereJson = {"status":{"lte":300},"spiderName":'baseSeSpider',"priority":{"$lt":1000}}
        mongoApt.remove(colName, whereJson=whereJson)
        
    def findKerwordsForSespider(self):
        '''
        加载Se爬虫的搜素关键字
        '''
        colName='KeyWord'
        return mongoApt.find(colName)
    
class OfflineApt(object):
    '''
    离线爬虫apt
    '''
    
    def findUnparsedPageByStatus(self): 
        '''
        查询待解析的Page，通过状态
        '''
        colName='PageDb'
        whereJson={'status':100} #,'spiderName':{'$nin':['sozhenSpider','bbkerSpider','mafengwoSpider','lvyou114Spider']}
        cursor = mongoApt.find(colName, whereJson=whereJson)
        return cursor
    
    def updatePageStatusAsSuccessById(self,pageId):
        '''
        更新PageDb的状态为解析成功状态
        '''
        colName='PageDb'
        mongoApt.update(colName, whereJson={'_id':ObjectId(pageId)}, updateJson={'status':200})
        
    def updatePageStatusAsUnsuccessById(self,pageId):
        '''
        更新PageDb的状态为解析失败状态
        '''
        colName='PageDb'
        mongoApt.update(colName, whereJson={'_id':ObjectId(pageId)}, updateJson={'status':101})
        
    def saveParsedItemToItemCollection(self,itemCollectionName,item):
        '''
        保存解析结果
        '''
        colName=itemCollectionName
        mongoApt.saveItem(colName, item)