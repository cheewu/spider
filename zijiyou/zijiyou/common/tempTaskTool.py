# encoding:utf-8
'''
Created on 2011-6-6
本工具用于临时任务的执行，如将PageDb中的url导入到UrlDb
@author: shiym
'''
from pymongo import objectid
from pymongo.connection import Connection
from zijiyou.common import utilities
from zijiyou.common.extractText import getText
from zijiyou.common.utilities import TxtDuplicateFilter, ProcessBar
import datetime

def dumpUrlFromPageDb2UrlDb(dbHost='localHost', port=27017, dbName='spiderV21', pageDbName='PageDb', urlDbName='UrlDb'):
    '''
    将PageDb中的url导入到UrlDb
    '''
    con = Connection(dbHost, port)
    db = con[dbName]
    pageCol = db[pageDbName]
    urlCol = db[urlDbName]
    #获得PageDb的游标
    pageDbCur = pageCol.find({}, {'url':1, 'spiderName':1})
    whereJson = {'url':''}
    counter = 0
    tolNum = pageDbCur.count()
    processBar=ProcessBar(numAll=tolNum)
#    thredHold = tolNum / 100
#    curNum = 0
#    percents = 0.0
    print '开始dump...总数量：%s' % tolNum
    for p in pageDbCur:
        processBar.printProcessBar()
#        curNum += 1
#        if curNum >= thredHold:
#            curNum = 0
#            percents += 1.0
#            print '当前进度：百分之%s' % percents
        url = p['url']
        if url == None or len(url) < 1:
            continue
        whereJson['url'] = url
        urlNum = urlCol.find(whereJson).count()
        if urlNum > 0:
            continue
        newUrl = {"url":url, "callBack":None, "reference":'PageDb', "status":200, "priority":1000, 'spiderName':p['spiderName'], "dateTime":datetime.datetime.now()}
        newUrl['md5'] = utilities.getFingerPrint([url], isUrl=True)
        newId = urlCol.insert(newUrl)
        counter += 1
        print '插入成功，新id：%s' % newId
    return counter 

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
#    thredHold = tolNum / 100
#    curNum = 0
#    percents = 0.0
    print '开始初始化md5值...总数量：%s' % tolNum
    for p in urlCur:
        #进度条
        processBar.printProcessBar()
#        curNum += 1
#        if curNum >= thredHold:
#            curNum = 0
#            percents += 1.0
#            print '当前进度：百分之%s' % percents
        url = p['url']
        md5Val = utilities.getFingerPrint([url], isUrl=True)
        whereJson = {'_id':p['_id']}
        uj = {'$set':{'md5':md5Val}}
        urlCol.update(whereJson, uj, True, False)

def checkDuplicatedContent(dbHost='192.168.0.183', port=27017, dbName='spiderV21', colName='Article', contentField='content'):
    '''
    检测colName表中contentField是否有重复
    '''
    if colName == '' or contentField == '':
        return
    con = Connection(dbHost, port)
    db = con[dbName]
    col = db[colName]
    cursor = col.find({}, {contentField:1}) #'md5':None
    dupChecker = TxtDuplicateFilter(md5SourceCols=[colName])
    #重复文本数
    numDup=0.0001
    #进度条
    tolNum=cursor.count()
    processBar=ProcessBar(numAll=tolNum,numUnit=100)
#    thredHold = numAll / 1000
#    curNum = 0
#    percents = 0.0
    print '开始对%s的字段%s检查重复...总数量：%s' % (colName,contentField,tolNum)
    for p in cursor:
        #进度条
        processBar.printProcessBar()
#        curNum += 1
#        if curNum >= thredHold:
#            curNum = 0
#            percents += 0.1
#            print '当前进度：百分之%s' % percents
            
        if not (contentField in p):
            continue
        content = p[contentField]
        #去掉html标签
        content = getText(content)
        isDup, md5 = dupChecker.checkDuplicate(p['_id'], content)
        if isDup:
            numDup+=1
        updateJson = {'$set':{'md5':md5, 'isDup':isDup}}
        whereJson = {'_id':objectid(p['_id'])}
        col.update(whereJson, updateJson)
    print '完成排重，数据集%s发现重复数量：%s 总文本数%s 重复比例%s' % (colName,numDup,tolNum,(numDup/tolNum))

def updateDaodaoResponseItemCollectionName(dbHost='192.168.0.183', port=27017, dbName='spiderV21', colName='PageDb'):
    '''
    更新道道网的response类型
    '''
    nameMap={'note':'Note','Note':'Note','attraction':'Attraction','Attraction':'Attraction'}
    #连接数据库
    con=Connection(dbHost,port)
    db=con[dbName]
    col=db[colName]
    cursor=col.find({'spiderName':'daodaoSpider'},{'itemCollectionName':1})
    #进度条
    tolNum = cursor.count()
    processBar=ProcessBar(numAll=tolNum)
#    thredHold = tolNum / 10000
#    curNum = 0
#    percents = 0.0
    print '总数量：%s' % tolNum
    for p in cursor:
        #进度条
        processBar.printProcessBar()
#        curNum += 1
#        if curNum >= thredHold:
#            curNum = 0
#            percents += 0.01
#            print '当前进度：百分之%s' % percents
        itemCollectionName=(p['itemCollectionName']).strip()
        updateJson={'$set':{'itemCollectionName':nameMap[itemCollectionName]}}
        whereJson={'_id':objectid(p['_id'])}
        col.update(whereJson,updateJson)

def dumpResponse2PageDb(dbHostSource='192.168.0.183', dbHostTarget='192.168.0.183',
                        portSource=27017, portTarget=27017,
                        dbNameSource='spidertest', dbNameTarget='spiderV21',
                        colNameSource='PageDb', colNameTarget='PageDb',
                        needMap=False):
    newField = 'newField'
    baseSchema = {'status':'status', 'pushDate':'pushDateTime',
                  'pushDateTime':'pushDateTime', 'dateTime':'optDateTime', 'spiderName':'spiderName',
                  'collectionName':'collectionName', 'collectionName':'itemCollectionName',
                  'itemCollectionName':'itemCollectionName'
                  }
    customSchema = {
              'CrawlUrl':{'url':'url', 'reference':'reference', 'callBack':'callBack', 'priority':'priority'},
              'responseCol':{'pageUrl':'url', 'type':'itemCollectionName', 'content':'responseBody', newField:'updateInterval'}
              }

    conSource = Connection(dbHostSource, portSource)
    conTarget = Connection(dbHostTarget, portTarget)
    dbSource = conSource[dbNameSource]
    dbTarget = conTarget[dbNameTarget]
    colSource = dbSource[colNameSource]
    colTarget = dbTarget[colNameTarget]
    cursor = colSource.find()
    tolNum = cursor.count()
    numAdd = 0
    numDup = 0
    processBar=ProcessBar(numAll=tolNum)
#    thredHold = numAll / 100
#    counter = 0
#    percents = 0.0
    print '开始从%s向%s Dump %s 数据量：%s' % (dbHostSource, dbHostTarget, colNameSource, tolNum)
    for p in cursor:
        #进度
        processBar.printProcessBar()
#        counter += 1
#        if counter >= thredHold:
#            counter = 0
#            percents += 1.0
#            print '当前进度：百分之%s' % percents
            
        url = ''
        if not ('url' in p):
            url = (p['pageUrl']).strip()
        elif isinstance(p['url'], list) and len(p['url']) > 0:
            url = (p['url'][0]).strip()
        else:
            url = (p['url']).strip()
        #判断是否重复
        number = colTarget.find({'url':url}).limit(1).count()
        #不重复，增加
        if number < 1:
            #字段是否需要做映射
            if not needMap:
                item = {}
                #处理字典类型，转为非字典类型
                for k, v in p.items():
                    #id自动生成
                    if k == '_id':
                        continue
                    elif isinstance(v, list) and len(v) > 0:
                        item[k] = v[0]
                    else:
                        item[k] = v
                colTarget.insert(item)
            else:
                item = {}
                #基础公共信息
                for bk, bv in  baseSchema.items():
                    if bk in p:
                        item[bv] = (p[bk]).strip()
                #数据集自定义字段映射
                custom = customSchema[colNameSource]
                if custom:
                    for ck, cv in custom.items():
                        if ck == newField:
                            item[cv] = None
                        elif ck in p:
                            item[cv] = (p[ck]).strip()
                    #补全必要字段：
                    item["spiderName"] = "daodaoSpider"
                    item["collectionName"] = "PageDb"
                    item["optDateTime"] = datetime.datetime.now()
                    item["status"] = 100
                colTarget.insert(item)
            numAdd += 1
        else:
            numDup += 1
    print '重复：%s' % numDup
    print '完成Dump，目标集合共增加了%s个新item' % numAdd
    
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
    if needDumUrl:
        print 'run urlDump ... '
        newNum = dumpUrlFromPageDb2UrlDb()
        print 'OK!-------------从PageDb向UrlDb插入个数%s----------------------OK!' % newNum
    if needInitUrl:
        print 'run urlInit ... '
        initUrlMd5()
        print 'OK!-------------urlMD5初始化完成----------------------OK!' 
    if needCheckDup:
        print 'run dupCheck ...'
#        checkDuplicatedContent(dbHost='192.168.0.183', port=27017, dbName='spiderV21', colName='POI', contentField='content')
        checkDuplicatedContent(dbHost='192.168.0.183', port=27017, dbName='spiderV21', colName='Note', contentField='content')
        checkDuplicatedContent(dbHost='192.168.0.183', port=27017, dbName='spiderV21', colName='Article', contentField='content')
        print 'OK ! -----------dupCheck完成------------------- OK!'
    if needDumpResposne:
        print 'run DumpResposne ...'
        dumpResponse2PageDb(dbNameSource='daodaoDb', colNameSource='responseCol', needMap=True)
        print 'OK ! -----------DumpResposne完成--------------- OK!'
    if needUpdateDaodao:
        print 'run updateDaodaoResponseItemCollectionName ...'
        updateDaodaoResponseItemCollectionName()
        print 'OK ! -----------updateDaodaoResponseItemCollectionName完成--------------- OK!'
    if needDumpKeyword:
        print 'run dumpKeyWordsFromDb ...'
        dumpKeyWordsFromDb()
        print 'OK ! -----------dumpKeyWordsFromDb--------------- OK!'
    
    
    print 'all tasks have been complecated!'
    
if __name__ == '__main__':
    run(needCheckDup=True)
    
    

