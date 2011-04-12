# -*- coding: utf-8 -*-
'''
Created on 2011-4-1

@author: shiym
'''
from pymongo import Connection
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured

class MongoDbApt(object):
    '''
    save the data in mongo
    '''
    
    dbHost=None
    port=27017
    con=None
    db=None
    dbCollections={}

    def __init__(self):
        '''
        init the dataBase
        '''
        print('++MongoDbApt++++++++++++++++++++++++++++++++++++')
        self.dbHost=settings.get("DB_HOST")
        dbName=settings.get("DB")
        dbCols=settings.get("DB_COLLECTIONS")
        self.port=settings.get("DB_PORT",27017)
        if not self.dbHost or len(dbCols)<1 or not dbName:
            raise NotConfigured
        
        #initiate the connection and the collection
        self.con=Connection(self.dbHost,self.port)
        self.db=self.con[dbName]
        for p in dbCols:
            self.dbCollections[p]=self.db[p]
        
    def saveItem(self,colName,item):
        '''
        save a single item. colName is the name of the collection. 
        '''
        return self.dbCollections[colName].insert(item)
        
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
    
    def findByDictionaryAndSort(self,colName,queJson,sortField):
        '''
        find and sort result(option) of mongodb
        '''
        if sortField:
            return self.db[colName].find(queJson).sort(sortField);
        else:
            return self.db[colName].find(queJson)
    
    def removeAll(self,colName):
        '''
        removeAll of mongodb
        '''
        return self.db[colName].remove({})
    
    def remove(self,colName,queJson):
        '''
        remove of mongodb
        '''
        return self.db[colName].remove(queJson)
    