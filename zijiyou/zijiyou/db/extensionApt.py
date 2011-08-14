# coding:utf-8
'''
Created on 2011-8-5
爬虫扩展程序的数据库适配器
@author: shiym
'''
from zijiyou.db.apt import mongoApt

class DiagnoserApt(object):
    '''
    爬虫诊断器的db适配器
    '''
    
    def countErrorStatusUrls(self):
        '''
        总下载失败网页数量
        '''
        colName='UrlDb'
        whereJson={'status':{'$gte':400,'$lt':900}}
        errorUrlNum=mongoApt.countByWhere(colName, whereJson=whereJson)
        return errorUrlNum
        
    def countUncrawlUrls(self):
        '''
        总剩余待爬取的网页数量
        '''
        colName='UrlDb'
        whereJson={'status':{'$gt':900}}
        uncrawlNum=mongoApt.countByWhere(colName, whereJson=whereJson)#self.mongo.countByWhere(colName, whereJson=whereJson)
        return uncrawlNum