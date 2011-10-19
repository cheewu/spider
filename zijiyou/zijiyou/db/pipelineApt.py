# coding:utf-8
'''
Created on 2011-8-14

@author: shiym
'''
from zijiyou.db.apt import mongoApt
class StorageApt(object):
    '''
    classdocs
    '''
    
    def saveItem(self,itemCollectionName,item,spiderName):
        return mongoApt.save(spiderName,itemCollectionName, item)