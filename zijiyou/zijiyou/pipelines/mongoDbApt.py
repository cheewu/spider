# -*- coding: utf-8 -*-
'''
Created on 2011-4-1

@author: shiym
'''
import pymongo
#import pymongo.Connection
#import scrapy.conf.settings
from scrapy.exceptions import NotConfigured

class MongoDbApt(object):
    '''
    save the data in mongo
    '''
    
    dbHost=None
    port=27017
    con=None
    dbs=None
    dbCollections=None

    def __init__(self):
        '''
        init the dataBase
        '''
        print('MongoDbApt+++++++++++++')
        '''
        self.dbHost=scrapy.conf.settings.get("DB_HOST")
        dbCols=scrapy.conf.settings.get("DB_COLLECTIONS")
        self.port=scrapy.conf.settings.get("DB_PORT",27017)
        if not self.dbHost or not len(self.dbCols)<1 :
            raise NotConfigured
        
        #initiate the connection and the collection
        self.con=pymongo.Connection(self.dbHost,self.port)
        for p in dbCols:
            self.dbCollections[p]=self.con[p]
        '''
        #test ImportError: No module named settings
        self.dbHost="localhost"
        con=pymongo.Connection(self.dbHost,self.port)
        self.dbs=con["daodaoDb"]
        self.dbCollections={"daodaoCol":self.dbs["daodaoCol"]}
        self.dbCollections["testCol"]=self.dbs["testCol"]
        
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
    
            
            
            