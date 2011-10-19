# coding:utf-8
'''
Created on 2011-8-14

@author: shiym
'''
#from zijiyou.db.apt import mongoApt

class UtilityApt(object):
    '''
    classdocs
    '''
    
    def findMd5sFromCollection(self,colName):
        '''
        初始化md5集合
        '''
        raise NotImplemented('未实现初始化md5集合')
#        whereJson={'status':{'$gt':0},'isDup':False}
#        fieldsJson={'md5':1}
#        cursor=mongoApt.find(colName, whereJson=whereJson, fieldsJson=fieldsJson)
#        return cursor
        
        