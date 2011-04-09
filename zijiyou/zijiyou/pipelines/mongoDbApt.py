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
        dbCols=settings.get("DB_COLLECTIONS")
        self.port=settings.get("DB_PORT",27017)
        dbName=settings.get("DB")
        if not self.dbHost or not len(dbCols)<1 or dbName:
            raise NotConfigured
        
        #initiate the connection and the collection
        self.con=Connection(self.dbHost,self.port)
        self.db=self.dbs[dbName]
        for p in dbCols:
            self.dbCollections[p]=self.dbDefault[p]
        
    def saveItem(self,colName,item):
        '''
        save a single item. colName is the name of the collection. 
        '''
        return self.dbCollections[colName].insert(item)
        
    def saveItems(self,colName,items):
        '''
        bulk save. colName is the name of the collection. 
        '''
        return self.dbCollections[colName].insert(items)
            