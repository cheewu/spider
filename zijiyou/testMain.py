# -*- coding: utf-8 -*-
#!/usr/bin/env python

#from collections import defaultdict
from pymongo.connection import Connection
from pymongo.objectid import ObjectId
from zijiyou.common.extractText import getText
from zijiyou.common.utilities import getFingerPrint, TxtDuplicateFilter, \
    ProcessBar
#from scrapy import log
#from scrapy.conf import settings
#from zijiyou.common.tempTaskTool import run
#from zijiyou.spiders.offlineCrawl.parse import Parse
#import datetime
#import hashlib
#import os
#import re
#import time
#run(needCheckDup=True)

def checkDuplicatedContent(dbHost='192.168.0.183', port=27017, dbName='spiderV21', colName='Article', contentField='content',needStrip=False):
    '''
    检测colName表中contentField是否有重复
    '''
    con = Connection(dbHost, port)
    db = con[dbName]
    col = db[colName]
    cursor = col.find({}, {contentField:1}) #'md5':None
    dupChecker = TxtDuplicateFilter(md5SourceCols=[])#colName
    #重复文本数
    numDup=0
    #进度条
    tolNum=cursor.count()
    processBar=ProcessBar(numAll=tolNum,numUnit=100)
    print '开始对%s的字段%s检查重复...总数量：%s' % (colName,contentField,tolNum)
    for p in cursor:
        #进度条
        processBar.printProcessBar()
        if not (contentField in p):
            continue
        content = p[contentField]
        #脏数据
        if len(content)>15000:
            continue
        #去掉html标签
        if needStrip:
            content = getText(content)
        isDup, md5 = dupChecker.checkDuplicate(p['_id'], content)
        if isDup:
            numDup+=1
        updateJson = {'$set':{'md5':md5, 'isDup':isDup}}
        whereJson = {'_id':ObjectId(p['_id'])}
        col.update(whereJson, updateJson)
    print '完成排重，数据集%s发现重复数量：%s 总文本数%s 重复比例：百分之%s' % (colName,numDup,tolNum,(numDup*100.0/tolNum))

checkDuplicatedContent(dbHost='192.168.0.183', port=27017, dbName='spiderV21', colName='Article', contentField='content')
checkDuplicatedContent(dbHost='192.168.0.183', port=27017, dbName='spiderV21', colName='Note', contentField='content')


def initItemMd5WithUrl(dbHost,dbName,colName):
    '''
    初始化item表的pid作为唯一主键
    '''
    con = Connection(dbHost, 27017)
    db = con[dbName]
    col = db[colName]
    cursor=col.find({'pid':{'$exists':False}})
    tolNum=cursor.count()
    processBar=ProcessBar(numAll=tolNum,numUnit=100)
    print '总数：%s' % tolNum
    for p in cursor:
        processBar.printProcessBar()
        whereJson={'_id':ObjectId(p['_id'])}
        pid=getFingerPrint(inputs=[p['url']], isUrl=True)
        updateJson={'$set':{'pid':pid}}
        col.update(whereJson, updateJson)
    print '完成 %s的pid初始化' % colName
initItemMd5WithUrl('192.168.0.183','spiderV21','Article')
initItemMd5WithUrl('192.168.0.183','spiderV21','Note')
print '全部完成'






#areas=['s','ssd','s3']
#areasNew=areas[1:len(areas)]
#print areasNew
#dic={
#  "_id": ObjectId("4e4814edd8091f7108843128"),
#  "articleId": "4e44fa9a4ccdb4610d0027d8",
#  "category": "介绍|0.8768079 ",
#  "collectionName": "Note",
#  "content": "　　来自欧洲城市博物馆和街头上那种与艺术珍藏近乎零距离欣赏所产生的艺术自由感，不同于书，不同于史，感受着文物的历史气息和艺术的思想熏陶，让我对博物馆的功能定位有了新的思考：今天的博物馆不应成为文物垄断的代名词。中国的历史很悠久，但能展示给社会大众的珍贵文物却很少，原因就在于藏宝于馆的惯有思维依然盛行。在这一点上，欧洲博物馆积极倡导的“推广、普及、研究、保护”式开放理念值得我们借鉴，博物馆社会化不仅可以丰富一个城市文化内涵和提高大众艺术品位，还能使原本就属于全社会宝贵遗产的历史文物更好地为时代发展服务。\n\n　　今天，我们与其在旅游景点上耗费大量钱财为将来制造越来越多的水泥钢筋式“文物”，不如以建立分馆的形式，将可分散保管的文物尽可能分流，好处至少有五点：一能避免群毁群损的现象发生，二能便于精心保管保养，三能提高文物的展览利用率，四能丰富分馆所在城市的文化内涵，五能增强社会大众的文物保护意识。何乐而不为呢！",
#  "keywords": "原因 旅游 展览 时代 服务 景点 全 思维 思想 艺术品 思考 欣赏 推广 城市 分散 保养 中国 艺术 大众 展示 保护 研究 史 历史 文化 欧洲 街头 珍藏 定位 自由 感受 开放 新 发展 博物馆 遗产 社会 气息 现象 文物 功能 感 ",
#  "publishDate": "2009年05月15日11:42",
#  "status": 220,
#  "title": "",
#  "url": "http:\/\/travel.people.com.cn\/GB\/9307796.html"
#}
#objId = mongoApt.saveItem('Note', item=dic)
#print objId

#t='- - - +856 212 530-3  -'
#match = re.search('\+(\d+) [0-9 -]+', t, 0)
#if match:
#    print match.group(0)
#    print match.group(1)
#s='ss：搜素：的'
#print s.split(u'：')
#mon=MongoDbApt()
#cursor = mon.findCursor('Region')
#for p in cursor:
#    updateJson={}
#    if 'name' in p:
#        names=p['name'].split('：')
#        if len(names)>0 :
#            updateJson['name']=names[-1]
#    if 'area' in p:
#        areas=p['area'].split('-')
#        if len(areas)>1:
#            areasNew=areasNew=areas[1:len(areas)]
#            updateJson['area']='-'.join(k for k in areasNew)
#        elif len(areas)==1:
#            updateJson['area']=areas[0]
#        
#    whereJson={'_id':ObjectId(p['_id'])}
#    mon.updateItem('Region', whereJson=whereJson, updateJson=updateJson)




#numUnit=1000
#print 100.0 / numUnit

#    else :
#        print '%s 啥类型也不是' %k
    
#    if  isinstance(v, {}):
#        print 'dict'
#    if isinstance(v, ''):
#        print 'String'

#conSource=Connection('192.168.0.183',27017)
#dbSource=conSource['spiderV21']
#dbSCol=dbSource['KeyWord']
##conTarget=Connection('127.0.0.1',27017)
##dbT=conTarget['spidertest']
##dbTCol=dbT['KeyWord']
#curS=dbSCol.find()
#print curS.count()
#i=1
#for cur in curS:
#    if i+1 < 10: 
#        print cur
#        i+=1
#    else:
#        break
#print 'ok!'
#for p in cursor:
#    print p

#p=Parse(isOffline=True)
#p.parse()

#alt="\u7ed7\ue0ff\u7af4\u7039\ue0a3\ue196\u95c6\u5d85\u7af7\u93b7\u590a\u608d__\u6d94\u6130\ufffd\u65c0\u68be\u5a13\u54e5\u7d89"
#t1=alt.decode('gb2312')
#print t1
#print 'OK??'
#apt = MongoDbApt()
#print 'OK!!'
#obj = apt.saveItem('test', {'name':'testtt'})
#print obj


#whereJson={'status':{'$gt':900}}
#crawlCol='UrlDb'
#mongo=MongoDbApt()
#um=mongo.countByWhere(crawlCol, whereJson)
#print 1.0 / um 
#print 1 / um

#t={'t1':'t11'}
#ps = defaultdict(int)
#ps['tt1'] +=1
#ps['tt2'] +=2
#print ps
#ps.clear()
#print ps
#keys=ps.keys()
#print 'keys:%s' % ps.keys()
#print 'key:%s' % t.keys()
#print len(ps)

#from zijiyou.items.zijiyouItem import PageDb,Article,Note
#pd=Note()
##pd['itemCollectionName']='100'
##pd['status']='100'
##pd['spiderName']='lvpingSpider'
##pd['spiderName']=100
#if pd.has_key('imageUrls'):#imageUrls
#    print 'ok'
#else:
#    print 'bad'
#pd.setdefault('status', 10000)
#print pd.get('status', 'baddd')
#pd['status']=20000
#print pd.get('status', 'baddd')
#print pd.get('collectionName')
#print pd['collectionName']

#mongo = MongoDbApt()
#value=mongo.findFieldsWithLimit('Article',whereJson={}, limitNum=1)
#print value
##print str(value['_id'])
#data={}
#data['add']=value[0]
#print value[0]['_id']
#print data
#encodeData=urlencode(data)
#print encodeData

#data=[{'add':{'id':1,'name':'a1'}},
#      {'add':{'id':2,'name':'a2'}},]
#data={'add':{'id':1,'name':'a1'},
#      'add2':{'id':2,'name':'a2'}}
#value=urlencode(data)
#print value

#def getFingerPrint(input):
#    '''
#        指纹
#    '''
#    hasher=hashlib.sha1(input)
##    hasher.update(canonicalize_url(str(input)))
#    fp=hasher.hexdigest()
#    return fp
#
#t=['www.baidu.com','www.baidu.com','www.google.com']
#v=set()
#for p in t:
#    fp=getFingerPrint(p)
#    if fp in v:
#        print '存在：%s' % p
#    else:
#        v.add(fp)
#        print '新的：%s' % p
#print v

#collectionNameMap={'Attraction':'POI',
#                                 'Hotel':'POI'}
#if 'Attraction' in collectionNameMap:
#    print collectionNameMap['Attraction']
#test={'a':'a1','b':'b1'}
#if 'a' in test:
#    print test['a']
#test=[]
#f='http://baidu.com.cnzijiyou.helloenummode%s'
#d1=datetime.datetime.now()
#for i in range(1,1500000):
#    test.append(f % i)
#t=set()
#for p in test:
#    if not p in t:
#        t.add(p)
#d2=datetime.datetime.now()
#print len(test)
#d=d2-d1
#print '%s,%s,%s' %(d1,d2, d.seconds)
    
#v=['aaa','bbb','aaa','abc']
#for p in v:
#    test.add(p)
#print test
#v1=['aaa','bbb','ccc']
#for p in v1:
#    if p in test:
#        print p
#    else:
#        print 'not:'


#content='首页-中国-22'
#print content.split('-')
#if len(content.split('-'))<3:
#    print 1
#else:
#    print 2
#parse=Parse()
#parse.parse()
#content='首页-中国-北京-北京景点'
#areaRegex=r'-(.*)-'
#p=re.compile(areaRegex)
#v=re.search(areaRegex,content,0)
#print v
#if v and v.group(1):
#    print v.group(1)
#v2=re.match(p, content,0)
#print v2
#if v2:
#    print v2.group(0)
#mon=MongoDbApt()
#colName='KeyWord'
#cur = mon.findFieldWithLimit(colName, limitNum=2)
#for p in cur :
#    print p

#print 'ok'

#test = settings.get('TESTLOG', '/home/shiym/test.txt')
#print test
#f=open(test,'a')
#f.write('test write3')
#f.close()
#f2=open(test,'r')
#print f2.readline()
#mon.removeAll(colName)


#urlTest='http://www.lvping.com/attractions-d152-guangzhou.html'
#matches = re.search(r'.*(attraction_review)+.*', urlTest)
#if not matches:
#    print 'cat'
#else:
#    print matches.group(0)

#for i in os.sys.path:
#    print i


#if not keyWords and len(keyWords)<1:
#    print ("没有关键字！")
#for keyWord in keyWords:
#    word='test' #=keyWord['keyWord']
#    encodeType='GBK' 
#    print word
#    encodeWords=urllib.quote(word.encode(encodeType))
#    print encodeWords
    
'''
查看数据
'''
#colSource=[
##           'ResponseBody',
##                '  'Attraction',
##                '  'Note',
##                '  'CrawlUrl',
##                '  'CommonSense'
##                '  'MemberInfo',
##                '  'MemberTrack',
##                '  'MemberFriend',
#                '  'MemberNoteList',
#                '  ]
#for i in range(0,len(colSource)):
#    print '(%s:%s)' %(colSource[i],mon.count(colSource[i]))
#    print ("%s" % mon.find(colSource[i], '', {'type':1}).limit(1)).encode('utf-8')
'''
测试离线爬虫的解析
'''
#parse=Parse()
#parse.parse()
#
#print 'ok'

'''模糊查询 日本'''
#regexAttraction='Attractions-g\d+-Activities-[oa\d-]+.*\.html$'#Attractions-g294232-Activities-oa1315-Japan.html Attractions-g\d+-Activities[-oa\d]+.*[Japan]+\.html$
##regexAttraction=r'^http:.*.html' Attractions-g\d+-Activities[-oa\d-]+.*\.html$
#                '#http://www.daodao.com/Attractions-g294232-Activities- Japan.html
#pattern=re.compile(regexAttraction)
##queJson={"url":{"$regex":regexAttraction}}
#queJson={"url":pattern}
#results = mon.findByDictionaryAndSort(colName, queJson, None)
#jq={'status': {'$gte': 300}, 'spiderName': 'daodaoSpider'}
#results =mon.findByDictionaryAndSort("CrawlUrl", jq,None)
#print len(results)
#i=0
#for p in results:
#    i+=1
#    if i <5:
#        print p

''''精确查询'''
#reg=r'http://www.daodao.com/Attraction_Review-g1066443-d1373705-Reviews-Chidorigafuchi-Chiyoda_Tokyo_Tokyo_Prefecture_Kanto.html'
#pattern=re.compile(reg)
#queJson={}
#results = mon.findByDictionaryAndSort('Attraction', queJson, None)
#print len(results)
#i=0
#for p in results:
#    i+=1
#    if i <5:
#        for p1 in p.keys():
#            print  p[p1]
'''造数据'''
#newResult=[]
#print len(newResult)
#mon.removeAll('test')
#values=[
#        {"url":"http://www.lvping.com/tourism-g29-Canada.html","order": 1},
#        {"url":"http://www.lvping.com/tourism-g90-ireland.html","order": 1},
#        {"url":"http://www.lvping.com/tourism-g44-philippine.html","order": 1},
#        {"reg":"(http://www.lvping.com/)?(tourism)+-g\d+-\w+\.html$","type":"国家","order": 1},
        
#        {"url":"http://www.lvping.com/travel-d29-sg1973/canada:Introduction.html","order": 2},
#        {"url":"http://www.lvping.com/travel-d90-sg13095/ireland:culture.html","order": 2},
#        {"url":"http://www.lvping.com/travel-d44-sg13141/philippine:climate.html","order": 2},
#        {"reg":"(http://www.lvping.com/)?(travel)+-d\d+-sg\d+/\w+:+\w+.*\.html$","type":"国家介绍 概况、气候等常识","order": 2},

#        {"url":"http://www.lvping.com/tourism-d1-beijing.html","order": 3},
#        {"url":"http://www.lvping.com/tourism-d356-Ottawa.html","order": 3},
#        {"url":"http://www.lvping.com/tourism-d352-MexicoCit.html","order": 3},
#        {"reg":"(http://www.lvping.com/)?(tourism-)+d\d+-\w+\.html$","type":"城市景区 a 介绍（目的地 介绍）","order": 3},
#        
#        {"url":"http://www.lvping.com/travel-d1-s11/Beijing:history.html","order": 4},
#        {"url":"http://www.lvping.com/travel-d1-s11118/Beijing:climate.html","order": 4},
#        {"url":"http://www.lvping.com/travel-d1-s12095/Beijing:culture.html","order": 4},
#        {"url":"http://www.lvping.com/travel-d1-s12095/Beijing:culture.html","order": 4},
#        {"reg":"(http://www.lvping.com/)?(travel-)+d1-+s\d+/\w+:\w+\.html$","type":"b.短文攻略(类别 内容 目的地)","order": 4},
#        
#        {"url":"http://www.lvping.com/attractions-d1-beijing.html","order": 5},
#        {"url":"http://www.lvping.com/attractions-d356-ottawa.html","order": 5},
#        {"url":"http://www.lvping.com/attractions-d352-mexicocity.html","order": 5},
#        {"reg":"(http://www.lvping.com/)?(attractions-)+d\d+-\w+\.html$","type":"景点列表","order": 5},
#        
#        {"url":"http://www.lvping.com/attraction_review-d1-s52626-detail.html","order": 6},
#        {"url":"http://www.lvping.com/attraction_review-d1-s230-detail.html","order": 6},
#        {"url":"http://www.lvping.com/attraction_review-d9-s1655-detail.html","order": 6},
#        {"reg":"(http://www.lvping.com/)?(attraction_review-)+d\d+-s\d+-detail\.html$","type":"a.介绍 经纬度","order": 6},
#        
#        {"url":"http://www.lvping.com/journals-d6158-s00-p1-g/laosjournals.html","order": 7},
#        {"reg":"(http://www.lvping.com/)?(journals-)+d\d+-s\d+-p\d+-g/\w+\.html$","type":"攻略列表","order": 7},
#        
#        {"url":"http://www.lvping.com/showjournal-d6158-r1322216-journals.html","order": 8},
#        {"reg":"(http://www.lvping.com/)?(showjournal-)+d\d+-r\d+-journals+\.html$","type":"a 作者 发表时间 浏览次数 评论次数","order": 8},
#        
#        {"url":"http://www.lvping.com/members/01C4DB3F897D414FA05AEF7D992EEE23","order": 9},
#        {"url":"http://www.lvping.com/members/pplvxingbao","order": 9},
#        {"reg":"(http://www.lvping.com/)?(members/)+\w+$","type":"用户","order": 9},
#        
#        {"url":"http://www.lvping.com/members/9EA06A1AF6DC4650A1F2A5C025A3ABA3/travelmap-public","order": 10},
#        {"reg":"(http://www.lvping.com/)?(members/)+(\w)+(/travelmap-public)+$","type":"足迹","order": 10},
#        
#        {"url":"http://www.lvping.com/members/pplvxingbao/friends","order":11},
#        {"reg":"(http://www.lvping.com/)?(members/)+(\w)+(/friends)+$","type":"好友","order":11},
#        
#        {"url":"http://www.lvping.com/members/01C4DB3F897D414FA05AEF7D992EEE23/journals","order":12},
#        {"reg":"(http://www.lvping.com/)?(members/)+(\w)+(/journals)+$","type":"游记',","order":12}
#       ]
#mon.saveItem('test', values)
##print 'count=%s:len=%s' %(mon.count('test'),len(values))
#
#'''测试url的reg'''
#regsJQ={'reg':re.compile(r".*")}#{"url":{"$regex":regexAttraction}}
#regs=mon.findByDictionaryAndSort("test", regsJQ,'order')
#for reg in regs:
#    print '*******************'
#    print 'order=%s,reg=%s' %(reg['order'],reg['reg'])
#    p = reg['reg']
#    pattern=re.compile(p)
#    results=mon.findByDictionaryAndSort('test', {'url':pattern}, None)
#    for result in results:
#        print result
#    print '------------------'
    


'''备份数据'''
#colSource=[
#           'daodaoCol', 
#           'crawlCol',
#           'noteCol'
#           ]
#colTarget=[
#           'daodaoColTest', 
#           'crawlColTest',
#           'noteColTest'
#           ]
#queJson={}
#
#for i in range(0,3):
#    mon.removeAll(colTarget[i])
#    print mon.count(colTarget[i])
#print '开始备份...'
#for i in range(0,3):
#    results=mon.findByDictionaryAndSort(colSource[i], queJson, None)
#    mon.saveItem(colTarget[i], results)
#    print mon.count(colTarget[i])
#print '完成备份1！'
#results=mon.findByDictionaryAndSort("responseCol", {}, None)
#print len(results)
#for p in results:
#    mon.saveItem("responseColTest", p)
#print mon.count("responseColTest")
#print '完成备份2！'
'''
清空爬到的数据
'''
#colSource=[
#                ''ResponseBody',
#                '  'Attraction',
#                '  'Note',
#                '  'CrawlUrl',
#                '  'CommonSense',
#                '  'MemberInfo',
#                '  'MemberTrack',
#                '  'MemberFriend',
#                '  'MemberNoteList',
#                '  'KeyWord',
#                '  'test']
#print '清空...'
#for i in range(0,len(colSource)):
#    print mon.count(colSource[i])
#    mon.removeAll(colSource[i])
#print '完成清空...'

#爬虫启动url
#startUrl = "http://www.lvping.com/members/jacobok"
#mon.remove('CrawlUrl', {"url":startUrl})
#value={"url":startUrl,"callBack":None,"status":400,"priority":1,"dateTime":datetime.datetime.now()}
#mon.saveItem('CrawlUrl', value)
#print mon.count("CrawlUrl")

#mon=MongoDbApt()
#item=[{'collectionName':'KeyWord','keyWord':'北京','itemCollectionName':'Article','priority':100,'pageNumber':15}]
#mon.saveItem('KeyWord', item)
#keyWords=mon.findByDictionaryAndSort('KeyWord', {}, 'priority')
#print len(keyWords)


#mon.removeAll(colName)
#mon.removeAll("daodaoCol")
#mon.removeAll("responseCol")
#mon.removeAll("crawlCol")
#mon.removeAll("noteCol")
#update
#whereJson={"priority":{"$gte":4000}}
#updateJson={"status":400}
#mon.updateItem(colName,whereJson,updateJson)

#queJson={}#"status":{"$gte":200}
#sortField="priority"
#results=mon.findByDictionaryAndSort(colName, queJson, sortField)
#print len(results)
#for p in results:
#    print p
#print 'find by id ++++++++++++++++++++++++++++++'
#queJson2={"_id":ObjectId("4da65b7b834fc00a6d000000")}
#results2=mon.findByDictionaryAndSort(colName, queJson2, sortField)
#for p in results2:
#    print p


#print 'findOne'
#print mon.findOne(colName)

#mon.removeAll(colName)
#testValue={"url":"www.daodao.com.lvyou",
#           "callBack":"parseOne",
#           "status":"0",
#           "priority":1}
#mon.saveItem(colName, testValue)
#print mon.count(colName)
#print mon.findOne(colName)
#whereJson={"url":"www.daodao.com.lvyou211"}
#updateJson={"status":"1"}
#mon.updateItem(colName, whereJson, updateJson)
#print 'updateItem OK'
#queJson={"status":"0"}
#sortField="priority"
#results=mon.findByDictionaryAndSort(colName, queJson, sortField)
#print len(results)
#print results
#
#'''
#print mon.testCount("daodaoCol")
#print mon.testCollectionNames()
#print mon.testFindOne("daodaoCol")
##mon.testRemove("daodaoCol", {"text":"My first blog post!"})
#mon.testRemoveAll("daodaoCol")
#print mon.testCount("daodaoCol")
#'''
#'''
#testValue={'area': ['\xe4\xba\x9a\xe6\xb4\xb2\n-\xe6\x97\xa5\xe6\x9c\xac\n-\xe5\x85\xb3\xe4\xb8\x9c\n-\xe4\xb8\x9c\xe4\xba\xac\xe9\x83\xbd\n-\xe4\xb8\x9c\xe4\xba\xac\n-\xe5\x8f\xb0\xe4\xb8\x9c\xe5\x8c\xba\n-\xe5\x8f\xb0\xe4\xb8\x9c\xe5\x8c\xba\xe6\x99\xaf\xe7\x82\xb9'], 
#           'pageUrl': ['http://www.daodao.com/Attraction_Review-g1066461-d321129-Reviews-Asakusa-Taito_Tokyo_Tokyo_Prefecture_Kanto.html'], 
#           'name': ['\n\xe6\xb5\x85\xe8\x8d\x89\n'], 
#           'address': ['\xe6\x97\xa5\xe6\x9c\xac-\xe5\x8f\xb0\xe4\xb8\x9c\xe5\x8c\xba'], 
#           'popularity': ['3']}
#
#print mon.saveItem("testCol", testValue)
#print mon.dbs.collection_names()
#print mon.dbCollections["testCol"].find_one()
#values=mon.dbCollections["testCol"].find()
#for val in values:
#    print('-------')
#    val
#    print('+++++++')
#'''
#
##print (mon.dbHost,mon.port,mon.dbs,mon.dbCollections)
#
#'''
#import re
#telNum='a\n\raa+81 3-3822-0111    '
#telNum1=re.match('(\+\d+[0-9 -]+)', telNum,0)
#telNum=re.search('\+\d+ [0-9 -]+', telNum, 0)
#if telNum1:
#    print telNum1
#if telNum:
#    print telNum.group(0)
#'''
#
#'''
#homePath=r'//div[@class="clearfix"]/div/div[@class="hotel-info clearfix"]/div[@class="leftContent"]'
#xpathItem={r'name':r'//div[@class="wrpHeader clearifix"]/h1[@id="HEADING"]/text()',
#           r'area':r'//div[@id="MAIN"]/div[class="crumbs"]/ul/li/ul/li/a/text()',
#           r'address':homePath+r'/div[@class="ar-detail"]/ul/li/span/text()',
#           r'desc':r'//div[@class="clearfix"]/div/div[@class="review-intro"]/text()',
#           r'popularity':homePath+r'/div[@class="ar-rank"]/span/text()',
#           r'telNum':homePath+r'/div[@class="ar-detail"]/ul/li/h3/text()'
#    }
#for k,v in xpathItem.items():
#    print k
#    print v
#    print('------------')
#from scrapy.cmdline import execute
#execute()
#'''
#
#'''
#import re
#s="共\naa1/30页"
#print s
#s2=re.sub(r'[\n\r\t]', '', s, 1)
#print '---'
#print (s2)
#m=re.search('/(\d+)', s, re.M)
##print m.group(1)
#li=['中文','b','c']
#li2=[]
#l=("-".join("%s" % p for p in li2)).encode("utf-8")
#print l
##for p in li:
##    li2.append(p.encode("utf-8"))
##li2.append("%s" % p.encode("utf-8") for p in li)
#
#colSource=['ResponseBody']
#dbName = "spiderV20"
#urlAttr = "pageUrl";
#testCon = pymongo.Connection("192.168.0.183", 27017)
#testSpiderDb = testCon[dbName]
#testResponse = testSpiderDb[colSource[0]]
#
##serverCon = pymongo.Connection("mongodb://zijiyou:zijiyou@58.83.134.166:27017/spiderV20")
#serverCon = pymongo.Connection("58.83.134.166", 27017)
#serverSpiderDb = serverCon[dbName]
#serverResponse = serverSpiderDb[colSource[0]]
#
#print "合并前，服务器数据库Response的count：", serverResponse.count()
#counter = 0
#
#for o in testResponse.find():
#    if urlAttr in o:
#        num = serverResponse.find({urlAttr:o[urlAttr]}).count()
#        if num<1:
#            serverResponse.insert(o)
#            counter += 1
#            print counter
##            if counter == 2:
##                'break
#    else:
#        print "没有pageUrl属性的记录ID：", o["_id"]
#            
#print "总共插入的记录数为：", counter
#print "183测试服务器数据库Response的count：", testResponse.count()
#print "服务器数据库Response的count：", serverResponse.count()

#清空国家、城市的列表页 CrawlUrl
#colSource=['CrawlUrl']
#dbName = "spiderV20"
#urlAttr = "url";
##
#serverCon = pymongo.Connection("mongodb://zijiyou:zijiyou@58.83.134.166:27017/spiderV20")
#serverCon = pymongo.Connection("58.83.134.166", 27017)
#serverSpiderDb = serverCon[dbName]
#serverResponse = serverSpiderDb[colSource[0]]
##
#counter = 0
#
#regex = [
##         r'http://www.lvping.com/NorthAmericaNavigation.aspx$',
##         r'http://www.lvping.com/EuropeNavigation.aspx$',
##         r'http://www.lvping.com/AsiaNavigation.aspx$',
##         r'http://www.lvping.com/ChinaNavigation.aspx$',
##         r'http://www.lvping.com/OceaniaNavigation.aspx$',
##         r'http://www.lvping.com/southAmericaNavigation.aspx$',
##         r'http://www.lvping.com/AfricaNavigation.aspx$',
#         r'(http://www.lvping.com/)?(tourism)+-g\d+-\w+\.html$', #国家
#         r'(http://www.lvping.com)?(/tourism-)+d\d+-\w+\.html$',  #城市:
##         r'(http://www.lvping.com)?/Journals.aspx\?type=1.*selecttype=0.*',# 精品游记列表
##         r'(http://www.lvping.com)?/Journals.aspx\?.*selecttype=2.*'# 攻略列表
#         ]
#
#print "更新前服务器数据库Response的count：", serverResponse.count()
#
#for r in regex:
#    count = serverResponse.find({urlAttr:{'$regex': r}}).count()
#    print count
#    serverResponse.remove({urlAttr:{'$regex': r}})
#            
#print "删除后服务器数据库Response的count：", serverResponse.count()

#print serverResponse.find({urlAttr:{'$regex': r'(http://www.lvping.com)?/Journals.aspx\?type=1.*selecttype=0.*'}}).count()


#正则匹配测试
#regex = [
#                                    {'regex':r'(http://www.lvping.com/)?(tourism)+-g\d+-\w+\.html$', 'priority':200}, #国家
#                                    {'regex':r'(http://www.lvping.com/)?(attractions-)+d\d+-\w+\.html$', 'priority':400}, #景点列表
#                                    {'regex':r'(http://www.lvping.com/)?(attractions-)+d\d+-s\d+-[r]+\w+\d+/\w+:\w+\.html$', 'priority':500}, #景点列表
#                                    {'regex':r'(http://www.lvping.com/)?(attractions-)+g\d+-\w+\.html$', 'priority':400}, #景点列表
#                                    {'regex':r'(http://www.lvping.com/)?(attractions-)+g\d+-[r]+\w+\d+-\w+\.html$', 'priority':450}, #景点列表
#                                    
##                                    {'regex':r'(http://www.lvping.com/)?(journals-)+d\d+-s\d+-p\d+-g/\w+\.html$', 'priority':1}, #攻略列表
#                                    {'regex':r'(http://www.lvping.com)?(/members/)+(\w/)+journals$', 'priority':1},# 会员游记列表
#                                    {'regex':r'(http://www.lvping.com)?/Journals.aspx\?type=1.*selecttype=0.*', 'priority':1},# 精品游记列表
#                                    {'regex':r'(http://www.lvping.com)?/Journals.aspx\?.*selecttype=2.*', 'priority':1},# 攻略列表
#                                    {'regex':r'(http://www.lvping.com/)?(travel-)+d\d+-\w+\.html$', 'priority':400},    #常识列表页1
#                                    {'regex':r'(http://www.lvping.com/)?(travel-)+d\d+-\w+:brochure\.html#\w+', 'priority':400}, #常识列表页2
#                                    {'type':'CommonSense','regex':r'(http://www.lvping.com/)?(travel)+-d\d+-s\w?\d+/\w+:+\w+.*\.html$', 'priority':1},  #国家介绍 概况、气候等常识
#                                  {'type':'Note','regex':r'(http://www.lvping.com/)?(travel-)+d1-+s\d+/\w+:\w+\.html$', 'priority':1}, #短文攻略(类别 内容 目的地)
#                                  {'type':'Note','regex':r'(http://www.lvping.com/)?(showjournal-)+d\d+-r\d+-journals+\.html$', 'priority':1}, #攻略 作者 发表时间 浏览次数 评论次数
#                                  {'type':'Note','regex':r'(http://www.lvping.com/)?journals/AllSingleJournals.aspx\?Writing=\d+', 'priority':1}, #第二种攻略游记情况 http://www.lvping.com/journals/AllSingleJournals.aspx?Writing=1322380
#                                  {'type':'MemberInfo','regex':r'(http://www.lvping.com/)?(members/)+\w+', 'priority':1}, #用户
#                                  {'type':'MemberTrack','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/travelmap-public)+$', 'priority':1}, #足迹
#                                  {'type':'MemberFriend','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/friends)+$', 'priority':1}, #好友
#                                  {'type':'MemberNoteList','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/journals)+$', 'priority':1},  #游记
#                                  
#                                  {'type':'Attraction','regex':r'(http://www.lvping.com/)?(attraction_review-)+d\d+-s\d+-[(detail)(attraction)]+\.html$', 'priority':1000}, #景点
#                                  {'type':'CityAttraction', 'regex':r'(http://www.lvping.com)?(/tourism-)+d\d+-\w+\.html$', 'priority':300}, #城市景区
#         ]
#
#
#for r in regex:
#    if re.search(r['regex'], 'http://www.lvping.com/members/memberlogin.aspx?url=http://www.lvping.com/members/default.aspx?screenname=82453902da154d5381bb3c514227ddea', 0):
#        print r['regex']


#colSource=['CrawlUrl']
#dbName = "spiderV20"
#urlAttr = "url";
##
#serverCon = pymongo.Connection("mongodb://zijiyou:zijiyou@58.83.134.166:27017/spiderV20")
#serverCon = pymongo.Connection("58.83.134.166", 27017)
#serverSpiderDb = serverCon[dbName]
#serverResponse = serverSpiderDb[colSource[0]]
#
#i = 0
#while i < 6:
#    print serverResponse.find({'status':200}).count()
#    i += 1
#    time.sleep(60)

#修改数据库shema   
#oldDbName = "spiderV20" 
#newDbName = "spiderV21"
#
#newField = 'newField'
#
#colMap = {
#          'CrawlUrl':'UrlDb',
#          'ResponseBody':'PageDb'
#          }
#
#baseSchema = {'status':'status', 'pushDate':'pushDateTime', 'spiderName':'spiderName', 'collectionName':'collectionName', 'dateTime':'optDateTime'}
#customSchema = {
#          'CrawlUrl':{'url':'url','reference':'reference', 'callBack':'callBack', 'priority':'priority'}, 
#          'ResponseBody':{'pageUrl':'url', 'type':'itemCollectionName', 'content':'responseBody', newField:'updateInterval'}
#          }
#
#serverCon = pymongo.Connection("192.168.0.183", 27017)
#oldDb = serverCon[oldDbName]
#newDb = serverCon[newDbName]
#
#
#counter = 0
#for k,v in colMap.items():
#    print "源集合：%s" % k, "新集合：%s" % v
#    counter = 0
#    for oldItem in oldDb[k].find(): 
#        item = {}
#        for bk, bv in  baseSchema.items():
#            if bk in oldItem:
#                item[bv] = oldItem[bk]
#        
#        custom = customSchema[k]
#        if custom:
#            for ck, cv in custom.items():
#                if ck == newField:
#                    item[cv] = None
#                else:
#                    if ck in oldItem:
#                        item[cv] = oldItem[ck]
#        
##        print oldItem
##        print item
#        newDb[v].insert(item)
#        counter += 1
#        print counter
#    print "新的集合：%s" % v, "共插入的数量为：%s" % counter
#        
#print "执行结束"
    



    
