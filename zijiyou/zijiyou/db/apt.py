# coding:utf-8
'''
Created on 2011-8-5

@author: shiym
'''
from pymongo import Connection,DESCENDING
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
    db={}
    #适配器
    
    def __init__(self):
        print '初始化Mongodb连接'
        dbHost=settings.get("DB_HOST")
        dbNameMap=settings.get("DB_MAP")
        port=settings.get("DB_PORT",27017)
        if not dbHost or len(dbNameMap)<1:
            log.msg("++初始化MongoDbApt失败！配置文件加载失败！++++++++++++++++++++++++++++++++++++",level=log.ERROR)
            raise NotConfigured
        #初始化
        self.con=Connection(dbHost,port)
        for k,v in dbNameMap.items():
            self.db[k]=self.con[v]
    
    def save(self,dbNameKey,colName,item={}):
        '''
        保存PageDb或url，返回id
        '''
        if len(item)<1:
            raise NotConfigured('空item！无法保存到表%s' % colName)
        objectId = self.db[dbNameKey][colName].insert(item)
        return objectId
    
    def countByWhere(self,dbNameKey,colName,whereJson={}):
        '''
        计算总数
        '''
        numTotal = self.db[dbNameKey][colName].find(whereJson).count()
        return numTotal
    
    def isExist(self,dbNameKey,colName,whereJson={}):
        '''
        判断是否存在
        '''
        num=self.db[dbNameKey][colName].find(whereJson).limit(1).count()
        if num>0:
            return True
        else:
            return False
    
    def getSingalFieldHits(self,dbNameKey,colName,fieldName='',whereJson={},sortField=None):
        '''
        查询指定记录的指定字段，返回结果集合，非游标
        '''
        cursor=None
        if sortField :
            cursor=self.db[dbNameKey][colName].find(whereJson,{fieldName:1}).sort(sortField)
        else:
            cursor=self.db[dbNameKey][colName].find(whereJson,{fieldName:1})
        results=[]
        for p in cursor:
            results.append(p[fieldName])
        return results
    
    def get(self,dbNameKey,colName,whereJson={},fieldNames=[]):
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
            cursor=self.db[dbNameKey][colName].find(whereJson,fieldNameJson) 
        else:
            cursor=self.db[dbNameKey][colName].find(whereJson) 
        results=[]
        for p in cursor:
            result={}
            for fieldName in fieldNames:
                result[fieldName]=p[fieldName]
            results.append(result)
        return results
    
    def find(self,dbNameKey,colName,whereJson={},fieldsJson=None,sortField=None,limitNum=0):
        '''
        查询，返回游标，可选择是否排序、是否查询全字段。 limitNum指定是否限制返回集合个数，0为不限制
        '''
        if sortField:
            if fieldsJson:
                return self.db[dbNameKey][colName].find(whereJson,fieldsJson).limit(limitNum).sort(sortField,direction=DESCENDING)
            else:
                return self.db[dbNameKey][colName].find(whereJson).limit(limitNum).sort(sortField,direction=DESCENDING)
        else:
            if fieldsJson:
                return self.db[dbNameKey][colName].find(whereJson,fieldsJson).limit(limitNum)
            else:
                return self.db[dbNameKey][colName].find(whereJson).limit(limitNum)
    
    def update(self,dbNameKey,colName,whereJson={},updateJson={}):
        '''
        更新
        '''
        if len(updateJson)<1:
            raise NotConfigured('数据集名为空，或updateJson为空，无法进行更新')
        updateJsonNew={"$set":updateJson}
        result = self.db[dbNameKey][colName].update(whereJson,updateJsonNew,multi=True)
        return result
        
    def remove(self,dbNameKey,colName,whereJson={}):
        '''
        删除
        '''
        return self.db[dbNameKey][colName].remove(whereJson) 

mongoApt=Mongodb() #mongodb数据库的适配器
