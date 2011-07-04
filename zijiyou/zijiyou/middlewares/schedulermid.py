# -*- coding: utf-8 -*-
'''
Created on 2011-5-24

@author: hy
'''
from httplib import HTTPConnection
from scrapy import log
from zijiyou.config.cookiesConfig import cookiesConfig
import datetime

class Cookies(object):
    _cookies = {}
    _cookiesStartTime = {}
    
    def enqueue_request(self,spider,request):
#        print 'scheduleMid test get:%s' % request.url
        cookies = self.getCookies(spider.name)
        if cookies and len(cookies)>1:
            request.cookies = cookies
            log.msg("开始调用cookies shedule中间件", log.DEBUG)
    
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

    