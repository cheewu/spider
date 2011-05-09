# -*- coding: utf-8 -*-
#!/usr/bin/env python

from bson.objectid import ObjectId
from zijiyou.db.mongoDbApt import MongoDbApt
from zijiyou.items.zijiyouItem import Attraction, CommonSense
from zijiyou.spiders.offlineCrawl.parse import Parse
from zijiyou.spiders.spiderConfig import spiderConfig
from zijiyou.spiders.offlineCrawl.parse import Parse
import datetime
import os
import re
import urllib
import pymongo
from scrapy.conf import settings
from scrapy import log

#parse=Parse()
#parse.parse()

#mon=MongoDbApt()
#colName='KeyWord'
#cur = mon.findFieldWithLimit(colName, limitNum=2)
#for p in cur :
#    print p
t={}
v= len(t.keys())>0 ? '1':'2'

print 'ok'

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

#item=[{'keyWord':'北京','type':'Note','priority':100}]
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
