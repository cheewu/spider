# -*- coding: utf-8 -*-
'''
Created on 2011-5-4

@author: shiym
'''
from scrapy.conf import settings
from scrapy import log
from zijiyou.db.mongoDbApt import MongoDbApt
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import datetime

class Diagnoser(object):
    '''
    故障诊断，对下列情形提出警告
    1.待爬取的网页数量低于阀值
    2.运行时间小于阀值，发出错误警告
    3.运行时间小于setting的时间间隔
    4.某些错误出现次数大于阀值
    警告写入日志
    '''
    
    def __init__(self):
        #某些错误出现次数
        self.errorCounter=0
        #某些错误出现次数下限阀值
        self.thresholdError=100
        #待爬取的网页数量下限阀值
        self.thresholdUntouchedUrl=20
        #运行时间下限阀值
        self.thresholdRuntime=200
        #setting的时间间隔
        self.closeSpiderTimeout=settings.get('CLOSESPIDER_TIMEOUT',1800)
        #警告文件路径
        self.diagnoserPath=settings.get('DIAGNOSER_PATH','./diagnosePath')
        self.errorStatus=[400]
        self.mongo=MongoDbApt()
        self.crawlCol='CrawlUrl'
        
        dispatcher.connect(self.onResponseReceived,signal=signals.response_received)
        dispatcher.connect(self.onSpiderClose,signal=signals.spider_closed)
        dispatcher.connect(self.onSpiderOpen,signal=signals.spider_opened)
    
    def onSpiderOpen(self,spider):
        self.biginTime=datetime.datetime.now()
        log.msg('onSpiderOpen %s' % spider.name,level=log.INFO)
                
    def onSpiderClose(self,spider,reson):
        endTime=datetime.datetime.now()
        intervalTemp=endTime - self.biginTime
        log.msg('onSpiderClose %s,intervalTemp=%s' % (spider.name,intervalTemp),level=log.INFO)
        interval=intervalTemp.hour * 3600 + intervalTemp.minute * 60 +intervalTemp.second
        if interval<self.thresholdRuntime:
            log.msg("警告：错误-运行时间小于阀值。运行时间：%s，间隔时间：%s" % (interval,self.closeSpiderTimeout), level=log.ERROR)
        elif (interval + 100) < self.closeSpiderTimeout:
            log.msg("警告：运行时间小于setting的时间间隔。运行时间：%s，间隔时间：%s" % (interval,self.closeSpiderTimeout), level=log.WARNING)
        
        whereJson={'status':1000}
        untouchedUrlNum=self.mongo.countByWhere(self.crawlCol, whereJson)
        if untouchedUrlNum<self.thresholdUntouchedUrl:
            log.msg("警告：错误-待爬取的网页数量低于阀值：%s" % untouchedUrlNum, level=log.ERROR)
        log.msg('onSpiderClose %s,intervalTemp=%s' % (spider.name,intervalTemp),level=log.INFO)
            
    def onResponseReceived(self,response,request,spider):
        if response.status in self.errorStatus:
            self.errorCounter+=1
        if self.errorCounter>self.thresholdError:
            log.msg("警告：错误-某些错误出现次数大于阀值：%s" % self.errorCounter, level=log.ERROR)
        print 'onResponseReceived %s,%s' % (spider.name,self.errorCounter)
            