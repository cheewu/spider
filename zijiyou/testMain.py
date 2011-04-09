# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pymongo
from zijiyou.pipelines.mongoDbApt import MongoDbApt
import datetime

mon=MongoDbApt()
print mon.testCount("daodaoCol")
print mon.testCollectionNames()
print mon.testFindOne("daodaoCol")
#mon.testRemove("daodaoCol", {"text":"My first blog post!"})
mon.testRemoveAll("daodaoCol")
print mon.testCount("daodaoCol")
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