# encoding:utf-8
'''
Created on 2011-6-6
本工具用于临时任务的执行，如将PageDb中的url导入到UrlDb
@author: shiym
'''
from pymongo.connection import Connection
from zijiyou.common import utilities
from zijiyou.common.utilities import ProcessBar

def initUrlMd5(dbHost='localHost', port=27017, dbName='spiderV21', urlDbName='UrlDb'):
    '''
    初始化urlDb的url的Md5值
    '''
    con = Connection(dbHost, port)
    db = con[dbName]
    urlCol = db[urlDbName]
    urlCur = urlCol.find({'md5':None}, {'url':1})
    #进度条
    tolNum = urlCol.find({'md5':None}).count()
    processBar=ProcessBar(numAll=tolNum)
    print '开始初始化md5值...总数量：%s' % tolNum
    for p in urlCur:
        #进度条
        processBar.printProcessBar()
        url = p['url']
        md5Val = utilities.getFingerPrint([url], isUrl=True)
        whereJson = {'_id':p['_id']}
        uj = {'$set':{'md5':md5Val}}
        urlCol.update(whereJson, uj, True, False)

def dumpKeyWordsFromDb(dbHost='192.168.0.183', port=27017, dbName='KeyWordDB', colName='KeyWord',
                       txtFileName='./keywords.txt'):
    con=Connection(dbHost,port)
    db=con[dbName]
    col=db[colName]
    cursor=col.find({},{'keyword':1})
#    #进度条
    tolNum = cursor.count()
    processBar=ProcessBar(numAll=tolNum)
    myFile=open(txtFileName,'w')
    for p in cursor:
        processBar.printProcessBar()
#        aline=p['keyword']+'， n ， 100， 0\n'
        aline=p['keyword']+'\n'
        myFile.write(aline)
    if not myFile.closed:
        myFile.close()
    
def run(needDumUrl=False, needInitUrl=False, needCheckDup=False, needDumpResposne=False,needUpdateDaodao=False,
        needDumpKeyword=False):
    print 'begin to run task!'
    
    print 'all tasks have been complecated!'
    
if __name__ == '__main__':
    run(needCheckDup=True)
    
    

