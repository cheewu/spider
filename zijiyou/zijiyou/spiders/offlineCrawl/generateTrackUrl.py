# encoding:utf-8
'''
Created on 2011-5-24

@author: hy
'''

from scrapy.conf import settings
from zijiyou.db.mongoDbApt import MongoDbApt
import datetime

def generateTrackUrl():
    mongoApt = MongoDbApt()
    trackUrlPrefix = "http://www.lvping.com/members/ajax/GetMyMap.ashx?gettype=getlall&profileUrlNO="
    pageDb = settings.get('RESPONSE_DB')
    urlDb = settings.get('CRAWL_DB')
    whereJson = {'itemCollectionName':'MemberInfo'}
    fieldsJson = {'url':1}
    memberUrls = mongoApt.findFieldsAndSort(pageDb, whereJson=whereJson, fieldsJson=fieldsJson)
    print 'MemberInfo count:', len(memberUrls)
    counter = 0
    for p in memberUrls:
#        print p['url']
        if p['url']:
            tmp = p['url'].split('/')
            if tmp:
                trackUrl = trackUrlPrefix + tmp[-1]
                item = {"callBack":None,"status":1000,"priority":1100,"dateTime":datetime.datetime.now(), "spiderName":"lvpingSpider", "reference":None}
                item['url'] = trackUrl
                mongoApt.saveItem(urlDb, item)
                counter += 1
    print 'Finish, track count:',counter

if __name__ == '__main__':
    generateTrackUrl()