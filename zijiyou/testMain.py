# -*- coding: utf-8 -*-
#!/usr/bin/env python

from bson.objectid import ObjectId
from zijiyou.db.mongoDbApt import MongoDbApt
import datetime
import pymongo

mon=MongoDbApt()
colName="crawlCol"
#mon.removeAll(colName)
#update
#whereJson={"priority":{"$gte":4000}}
#updateJson={"status":400}
#mon.updateItem(colName,whereJson,updateJson)

queJson={"status":{"$gte":200}}#
sortField="priority"
results=mon.findByDictionaryAndSort(colName, queJson, sortField)
print len(results)
for p in results:
    print p
print 'find by id ++++++++++++++++++++++++++++++'
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

'''
print mon.testCount("daodaoCol")
print mon.testCollectionNames()
print mon.testFindOne("daodaoCol")
#mon.testRemove("daodaoCol", {"text":"My first blog post!"})
mon.testRemoveAll("daodaoCol")
print mon.testCount("daodaoCol")
'''
'''
testValue={'area': ['\xe4\xba\x9a\xe6\xb4\xb2\n-\xe6\x97\xa5\xe6\x9c\xac\n-\xe5\x85\xb3\xe4\xb8\x9c\n-\xe4\xb8\x9c\xe4\xba\xac\xe9\x83\xbd\n-\xe4\xb8\x9c\xe4\xba\xac\n-\xe5\x8f\xb0\xe4\xb8\x9c\xe5\x8c\xba\n-\xe5\x8f\xb0\xe4\xb8\x9c\xe5\x8c\xba\xe6\x99\xaf\xe7\x82\xb9'], 
           'pageUrl': ['http://www.daodao.com/Attraction_Review-g1066461-d321129-Reviews-Asakusa-Taito_Tokyo_Tokyo_Prefecture_Kanto.html'], 
           'name': ['\n\xe6\xb5\x85\xe8\x8d\x89\n'], 
           'address': ['\xe6\x97\xa5\xe6\x9c\xac-\xe5\x8f\xb0\xe4\xb8\x9c\xe5\x8c\xba'], 
           'popularity': ['3']}

print mon.saveItem("testCol", testValue)
print mon.dbs.collection_names()
print mon.dbCollections["testCol"].find_one()
values=mon.dbCollections["testCol"].find()
for val in values:
    print('-------')
    val
    print('+++++++')
'''

#print (mon.dbHost,mon.port,mon.dbs,mon.dbCollections)

'''
import re
telNum='a\n\raa+81 3-3822-0111    '
telNum1=re.match('(\+\d+[0-9 -]+)', telNum,0)
telNum=re.search('\+\d+ [0-9 -]+', telNum, 0)
if telNum1:
    print telNum1
if telNum:
    print telNum.group(0)
'''

'''
homePath=r'//div[@class="clearfix"]/div/div[@class="hotel-info clearfix"]/div[@class="leftContent"]'
xpathItem={r'name':r'//div[@class="wrpHeader clearifix"]/h1[@id="HEADING"]/text()',
           r'area':r'//div[@id="MAIN"]/div[class="crumbs"]/ul/li/ul/li/a/text()',
           r'address':homePath+r'/div[@class="ar-detail"]/ul/li/span/text()',
           r'desc':r'//div[@class="clearfix"]/div/div[@class="review-intro"]/text()',
           r'popularity':homePath+r'/div[@class="ar-rank"]/span/text()',
           r'telNum':homePath+r'/div[@class="ar-detail"]/ul/li/h3/text()'
    }
for k,v in xpathItem.items():
    print k
    print v
    print('------------')
from scrapy.cmdline import execute
execute()
'''

'''
import re
s="共\naa1/30页"
print s
s2=re.sub(r'[\n\r\t]', '', s, 1)
print '---'
print (s2)
m=re.search('/(\d+)', s, re.M)
#print m.group(1)
li=['中文','b','c']
li2=[]
l=("-".join("%s" % p for p in li2)).encode("utf-8")
print l
#for p in li:
#    li2.append(p.encode("utf-8"))
#li2.append("%s" % p.encode("utf-8") for p in li)

'''