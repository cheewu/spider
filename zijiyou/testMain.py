# -*- coding: utf-8 -*-
#!/usr/bin/env python

from bson.objectid import ObjectId
from zijiyou.db.mongoDbApt import MongoDbApt
import datetime
from zijiyou.spiders.offlineCrawl.parse import Parse
from zijiyou.spiders.spiderConfig import spiderConfig
from zijiyou.items.zijiyouItem import Attraction,CommonSense


mon=MongoDbApt()
'''
查看数据
'''
#colSource=['ResponseBody',
##                  'Attraction',
##                  'Note',
#                  'CrawlUrl',
#                  'CommonSense']
#for i in range(0,len(colSource)):
#    print '(%s:%s)' %(colSource[i],mon.count(colSource[i]))
#    print mon.findOne(colSource[i])
'''
测试离线爬虫的解析
'''
#parse=Parse()
#parse.parse()

'''模糊查询 日本'''
#regexAttraction='Attractions-g\d+-Activities-[oa\d-]+.*\.html$'#Attractions-g294232-Activities-oa1315-Japan.html Attractions-g\d+-Activities[-oa\d]+.*[Japan]+\.html$
##regexAttraction=r'^http:.*.html' Attractions-g\d+-Activities[-oa\d-]+.*\.html$
#                #http://www.daodao.com/Attractions-g294232-Activities- Japan.html
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
#mon.removeAll(colName)
#value=[{"url":"http://www.daodao.com/Lvyou","order":1},
#       {"url":"http://www.daodao.com/Tourism-g294232-Japan-Vacations.html","order":2},
#       {"url":"http://www.daodao.com/Attractions-g294232-Activities-Japan.html","order":3},
#       {"url":"http://www.daodao.com/Attractions-g294232-Activities-oa15-Japan.html","order":4},
#       {"url":"http://www.daodao.com/Attractions-g298184-Activities-Tokyo_Tokyo_Prefecture_Kanto.html","order":5},
#       {"url":"http://www.daodao.com/Attractions-g298115-Activities-oa15-Kanazawa_Ishikawa_Prefecture_Chubu.html","order":6},
#       {"url":"http://www.daodao.com/Attraction_Review-g1066443-d1373705-Reviews-Chidorigafuchi-Chiyoda_Tokyo_Tokyo_Prefecture_Kanto.html","order":7}
#       ]
#print mon.saveItem(colName, value)
#print mon.count(colName)
#print mon.findOne(colName)

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
#colSource=['ResponseBody',
#                  'Attraction',
#                  'Note',
#                  'CrawlUrl',
#                  'CommonSense',
#                  'test']
#print '清空...'
#for i in range(0,len(colSource)):
#    print mon.count(colSource[i])
#    mon.removeAll(colSource[i])
#print '完成清空...'
#
##爬虫启动url
#mon.remove(colName, {"url":"http://www.daodao.com/Lvyou"})
#value={"url":"http://www.daodao.com/Lvyou","callBack":None,"status":400,"priority":1,"dateTime":datetime.datetime.now()}
#mon.saveItem(colName, value)
#print mon.count("crawlCol")




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
#'''