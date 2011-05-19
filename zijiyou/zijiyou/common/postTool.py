# -*- coding: utf-8 -*-
'''
Created on 2011-5-16

@author: shiym
'''
from zijiyou.db.mongoDbApt import MongoDbApt

from urllib2 import urlopen
from urllib2 import URLError
from urllib import urlencode

class PostData(object):
    '''
    推送数据
    '''

    def __init__(self,url='http://192.168.0.183:8080/solr3.1.0/core1/update'):
        self.defaultDataType='application/xml';
        self.dataModeFile='files'
        self.dataModeArgs='args'
        self.defaultDataMode='args'
        self.url=url
#        self.data={}
        self.postColNames=['Article']
        self.mongo=MongoDbApt()
        
    def post(self):
        '''
        数据推送
        '''
        print '开始推送'
        if self.defaultDataMode==self.dataModeFile:
            pass;
        elif self.defaultDataMode==self.dataModeArgs:
            counter=0
            counter+=1
            where={'status':100}
            whereUpd={}
            updateSuc={'$set':{'status':200}}
            updateFail={'$set':{'status':101}}
            data={'add':{}}
            for colName in self.postColNames:
                tolNum=self.mongo.countByWhere(colName, whereJson=where)
                count=0
                while count < tolNum:
                    value=self.mongo.findFieldsWithLimit(colName,whereJson=where, limitNum=1)
                    if not value or len(value)<1:
                        continue
                    data['add']['doc']=value[0]
                    whereUpd['_id']=value[0]['_id']
                    try:
                        encodeData=urlencode(data)
                        fileHander=urlopen(self.url, data=encodeData,timeout=3)
                        info=fileHander.info()
                        print '第%s次推送。目标url:。info：%s' % (counter,fileHander.geturl(),info)
                    except URLError, e:
                        print '第%s次推送。错误:。异常：%s' % (counter,str(e))
                        self.mongo.updateItem(colName, whereJson=whereUpd, updateJson=updateFail)
                    count+=1
                    counter+=1
                    self.mongo.updateItem(colName, whereJson=whereUpd, updateJson=updateSuc)
                print '完成对表%s的数据推送' % colName
        self.commit()
        print '结束推送'
            
    def commit(self):
        '''
        向solr提交
        '''
        encodeData='<commit/>'#urlencode('<commit/>')
        try:
            fileHander=urlopen(self.url, data=encodeData,timeout=5)
            info=fileHander.info()
            print '提交完成 info：%s' % (info)
        except URLError, e:
            print '提交失败 info：%s' % str(e)
    def test(self):
        data=r'{"add":{"doc":{"id":110,"title":"test"}}}'
#        value=urlencode(data)
        try:
#            fileHander=urlopen(self.url, data=data,timeout=5)

            url='http://192.168.0.183:8080/solr3.1.0/core1/select?q=cat:book'
            fileHander=urlopen(self.url,timeout=5)
            info=fileHander.info()
            print '提交完成 info：%s' % (info)
        except URLError, e:
            print '提交失败 info：%s' % str(e)
    
post=PostData()
post.test() 