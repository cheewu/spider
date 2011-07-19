# -*- coding: utf-8 -*-
'''
Created on 2011-4-1

@author: shiym
'''
from pymongo import Connection, DESCENDING
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
import gc

class MongoDbApt(object):
    '''
    save the data in mongo
    '''
    
    def __init__(self):
        '''
        init the dataBase
        '''
        log.msg("++初始化MongoDbApt++++++++++++++++++++++++++++++++++++",level=log.INFO)
        self.dbHost=settings.get("DB_HOST")
        dbName=settings.get("DB")
        dbCols=settings.get("DB_COLLECTIONS")
        self.port=settings.get("DB_PORT",27017)
        if not self.dbHost or len(dbCols)<1 or not dbName:
            log.msg("++初始化MongoDbApt失败！配置文件加载失败！++++++++++++++++++++++++++++++++++++",level=log.ERROR)
            raise NotConfigured
        
        #initiate the connection and the collection
        self.con=Connection(self.dbHost,self.port)
        self.db=self.con[dbName]
        self.dbCollections={}
        for p in dbCols:
            self.dbCollections[p]=self.db[p]
        
    def saveItem(self,colName,item):
        '''
        save a single item. colName is the name of the collection. 
        '''
        objectId = self.dbCollections[colName].insert(item)
        return objectId
        
    def findOne(self,colName):
        '''
        find_one of mongodb
        '''
        return self.db[colName].find_one()
        
    def count(self,colName):
        '''
        count of mongodb
        '''
        return self.db[colName].count()
    
    def countByWhere(self,colName,whereJson):
        return self.db[colName].find(whereJson).count()
    
    def isExist(self,colName,queJson):
        num=self.db[colName].find(queJson).count()
#        return num
        if num>0:
            return True
        else:
            return False
    
    def findTestCursor(self,colName,whereJson):
        return self.db[colName].find(whereJson)
    
    def findByDictionaryAndSort(self,colName,whereJson={},sortField=None):
        '''
        find and sort result(option) of mongodb
        sortField:排序字段，None表示不排序
        '''
        mycursor=None
        if sortField:
            mycursor = self.db[colName].find(whereJson).sort(sortField,direction=DESCENDING)           
        else:
            mycursor = self.db[colName].find(whereJson)
        
        results=[]
        if mycursor:
            for p in mycursor:
                results.append(p)
        return results
        
    def findFieldsAndSort(self,colName,whereJson={},fieldsJson={},sortField=None):
        '''
        find and sort result(option) of mongodb
        sortField:排序字段，None表示不排序
        '''
        mycursor=None
        if sortField:
            mycursor = self.db[colName].find(whereJson,fieldsJson).sort(sortField,direction=DESCENDING)        
        else:
            mycursor = self.db[colName].find(whereJson,fieldsJson)
        
        results=[]
        if mycursor:
            for p in mycursor:
                results.append(p)
        return results
    
    def findCursor(self,colName=None,whereJson={},fieldsJson={}):
        cursor = self.db[colName].find(whereJson,fieldsJson)
        return cursor 
    
    def findFieldsWithLimit(self,colName,whereJson={},limitNum=-1):
        mycursor=None
        if limitNum>0:
            mycursor = self.db[colName].find(whereJson).limit(limitNum)           
        else:
            mycursor = self.db[colName].find(whereJson)
        
        results=[]
        if mycursor:
            for p in mycursor:
                results.append(p)
        return results
    
    def updateItem(self,colName,whereJson,updateJson):
        '''
        更新
        '''
        uj={"$set":updateJson}
        result = self.db[colName].update(whereJson,uj,multi=True)#,False,True
        return result
        
    def removeAll(self,colName):
        '''
        removeAll of mongodb
        '''
        return self.db[colName].remove({})
    
    def remove(self,colName,whereJson):
        '''
        remove of mongodb
        '''
        if not (whereJson and len(whereJson)>0):
            return
        return self.db[colName].remove(whereJson)
    