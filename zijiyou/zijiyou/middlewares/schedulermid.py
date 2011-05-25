# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

cann't custom the scheduleMiddleWare, or spider cann't get start!
@author: shiym
'''
#from scrapy import log
#from zijiyou.db.mongoDbApt import MongoDbApt
#import datetime
#
#class RequestSaver(object):
#    '''
#    新调度保存入数据库
#    '''
#    mongoApt=None
#    colName="crawlCol"
#    def __init__(self):
#        if not self.mongoApt:
#            self.mongoApt=MongoDbApt()
#
#    def enqueue_request(self,spider,request):
##        log.msg("开始调用schedulermid中间件",level=log.INFO)
#        recentReq={"url":"","callBack":None,"status":"","priority":1,"dateTime":datetime.datetime.now()}
#        recentReq["url"]=request.url
#        meta=request.meta
#        if meta and "callBack" in meta:
#            recentReq["callBack"]=request.meta["callBack"]
#        recentReq["priority"]=request.priority
#        recentReq["status"]=1000
#        
#        queJson={"url":request.url}
#        if not self.mongoApt.isExist(self.colName, queJson):
#            self.mongoApt.saveItem(self.colName,recentReq)
#            log.msg("保存新request：%s" % request.url,level=log.INFO)
#        return None
    
'''
Created on 2011-5-24

@author: hy
'''
from httplib import HTTPConnection
from scrapy import log
from zijiyou.spiders.cookiesConfig import cookiesConfig
import datetime

class Cookies(object):
    _cookies = {}
    _cookiesStartTime = {}
    
    def enqueue_request(self,spider,request):
        log.msg("开始调用cookies shedule中间件", log.DEBUG)
#        print "开始调用cookies shedule中间件"
        request.cookies = self.getCookies(spider.name)
    
    def getCookies(self, spiderName):
        if spiderName in cookiesConfig:
            if not "domain" in cookiesConfig[spiderName] or not "url" in cookiesConfig[spiderName] or not "timeout" in cookiesConfig[spiderName]:
                log.msg("%s 的 cookiesConfig配置不正确" % spiderName, log.ERROR)
                return {}
            config = cookiesConfig[spiderName]
            cookiesEndTime = datetime.datetime.now()
            if (not spiderName in self._cookies) or (not spiderName in self._cookiesStartTime) or (cookiesEndTime - self._cookiesStartTime[spiderName]).seconds > config["timeout"]:
                print "get new cookie"
                log.msg("%s 获得新的cookies" % spiderName, log.INFO)
                self._cookiesStartTime[spiderName] = cookiesEndTime
                self._cookies[spiderName] = {}
#                print config["domain"]
#                print config["url"]
                conn = HTTPConnection(config["domain"])
                conn.request("HEAD", config["url"])
                resp = conn.getresponse()
                conn.close()
                cks = resp.getheader("set-cookie")
                print "new cookies：", cks
                if cks:
                    for v in cks.split(';'):
                        ck = v.split('=')
                        if ck and len(ck) == 2:
                            self._cookies[spiderName][ck[0].strip()] = ck[1].strip()
#            print self._cookies[spiderName]
            return self._cookies[spiderName]
        else:
            return {}

    