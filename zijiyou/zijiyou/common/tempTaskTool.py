# encoding:utf-8
'''
Created on 2011-6-6
本工具用于临时任务的执行，如将PageDb中的url导入到UrlDb
@author: shiym
'''
from pymongo.connection import Connection
from zijiyou.common import utilities 
import datetime

def dumpUrlFromPageDb2UrlDb(dbHost='localHost',port=27017,dbName='spiderV21',pageDbName='PageDb',urlDbName='UrlDb'):
    '''
    将PageDb中的url导入到UrlDb
    '''
    con=Connection(dbHost,port)
    db=con[dbName]
    pageCol=db[pageDbName]
    urlCol=db[urlDbName]
    #获得PageDb的游标
    pageDbCur=pageCol.find({},{'url':1,'spiderName':1})
    whereJson={'url':''}
    counter=0
    tolNum=pageDbCur.count()
    thredHold=tolNum/100
    curNum=0
    percents=0.0
    print '开始dump...总数量：%s' % tolNum
    for p in pageDbCur:
        curNum+=1
        if curNum >= thredHold:
            curNum=0
            percents+=1.0
            print '当前进度：百分之%s' % percents
        url=p['url']
        if url == None or len(url)<1:
            continue
        whereJson['url']=url
        urlNum=urlCol.find(whereJson).count()
        if urlNum>0:
            continue
        newUrl={"url":url,"callBack":None,"reference":'PageDb',"status":200,"priority":1000,'spiderName':p['spiderName'],"dateTime":datetime.datetime.now()}
        newUrl['md5']=utilities.getFingerPrint([url], isUrl=True)
        newId = urlCol.insert(newUrl)
        counter+=1
        print '插入成功，新id：%s' % newId
    return counter 

def initUrlMd5(dbHost='localHost',port=27017,dbName='spiderV21',urlDbName='UrlDb'):
    '''
    初始化urlDb的url的Md5值
    '''
    con=Connection(dbHost,port)
    db=con[dbName]
    urlCol=db[urlDbName]
    urlCur=urlCol.find({'md5':None},{'url':1})
    tolNum=urlCol.find({'md5':None}).count()
    thredHold=tolNum/100
    curNum=0
    percents=0.0
    print '开始初始化md5值...总数量：%s' % tolNum
    for p in urlCur:
        curNum+=1
        if curNum >= thredHold:
            curNum=0
            percents+=1.0
            print '当前进度：百分之%s' % percents
        url=p['url']
        md5Val=utilities.getFingerPrint(url, isUrl=True)
        whereJson={'_id':p['_id']}
        uj={'$set':{'md5':md5Val}}
        urlCol.update(whereJson,uj,True,False)
    
def run(needDumUrl=False,needInitUrl=False):
    print 'begin to run task!'
    if needDumUrl:
        print 'run urlDump ... '
        newNum = dumpUrlFromPageDb2UrlDb()
        print 'OK!-------------从PageDb向UrlDb插入个数%s----------------------OK!' %newNum
    if needInitUrl:
        print 'run urlInit ... '
        initUrlMd5()
        print 'OK!-------------urlMD5初始化完成----------------------OK!' 
    
    