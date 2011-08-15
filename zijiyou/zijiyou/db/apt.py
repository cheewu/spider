# coding:utf-8
'''
Created on 2011-8-5

@author: shiym
'''
from pymongo import Connection
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured

class Mongodb(object):
    '''
    mongodb的数据库适配器
    '''
    #连接器
    con=None
    #数据库
    db=None
    #适配器
    
    def __init__(self):
        print '初始化Mongodb连接'
        dbHost=settings.get("DB_HOST")
        dbName=settings.get("DB")
        port=settings.get("DB_PORT",27017)
        if not dbHost or not dbName:
            log.msg("++初始化MongoDbApt失败！配置文件加载失败！++++++++++++++++++++++++++++++++++++",level=log.ERROR)
            raise NotConfigured
        
        #initiate the connection and the collection
        self.con=Connection(dbHost,port)
        self.db=self.con[dbName]
    
    def saveItem(self,colName,item={}):
        '''
        保存item，返回id
        '''
        if len(item)<1:
            raise NotConfigured('空item！无法保存到表%s' % colName)
        objectId = self.db[colName].insert(item)
        return objectId
    
    def countByWhere(self,colName,whereJson={}):
        '''
        计算总数
        '''
        numTotal = self.db[colName].find(whereJson).count()
        return numTotal
    
    def isExist(self,colName,whereJson={}):
        '''
        判断是否存在
        '''
        num=self.db[colName].find(whereJson).limit(1).count()
        if num>0:
            return True
        else:
            return False
    
    def getSingalFieldHits(self,colName,fieldName='',whereJson={},sortField=None):
        '''
        查询指定记录的指定字段，返回结果集合，非游标
        '''
        cursor=None
        if sortField :
            cursor=self.db[colName].find(whereJson,{fieldName:1}).sort(sortField)
        else:
            cursor=self.db[colName].find(whereJson,{fieldName:1})
        results=[]
        for p in cursor:
            results.append(p[fieldName])
        return results
    
    def get(self,colName,whereJson={},fieldNames=[]):
        '''
        查询指定记录的指定字段，返回结果集合，非游标
        '''
        cursor=None
        #初始化查询字段
        fieldNameJson={}
        if len(fieldNames) > 0:
            for p in fieldNames:
                fieldNameJson[p]=1
        #执行查询
        if len(fieldNameJson)>0:
            cursor=self.db[colName].find(whereJson,fieldNameJson) 
        else:
            cursor=self.db[colName].find(whereJson) 
        results=[]
        for p in cursor:
            result={}
            for fieldName in fieldNames:
                result[fieldName]=p[fieldName]
            results.append(result)
        return results
    
    def find(self,colName,whereJson={},fieldsJson={},sortField=None,limitNum=0):
        '''
        查询，返回游标，可选择是否排序、是否查询全字段。 limitNum指定是否限制返回集合个数，0为不限制
        '''
        if sortField:
            if fieldsJson:
                return self.db[colName].find(whereJson,fieldsJson).limit(limitNum).sort(sortField)
            else:
                return self.db[colName].find(whereJson).limit(limitNum).sort(sortField)
        else:
            if fieldsJson:
                return self.db[colName].find(whereJson,fieldsJson).limit(limitNum)
            else:
                return self.db[colName].find(whereJson).limit(limitNum)
    
    def update(self,colName,whereJson={},updateJson={}):
        '''
        更新
        '''
        if len(updateJson)<1:
            raise NotConfigured('数据集名为空，或updateJson为空，无法进行更新')
        updateJsonNew={"$set":updateJson}
        result = self.db[colName].update(whereJson,updateJsonNew,multi=True)
        return result
        
    def remove(self,colName,whereJson={}):
        '''
        删除
        '''
        return self.db[colName].remove(whereJson) 

mongoApt=Mongodb() #mongodb数据库的适配器
