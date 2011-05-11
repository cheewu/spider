# -*- coding: utf-8 -*-
'''
Created on 2011-5-4

@author: shiym
'''
from scrapy import log, signals
from scrapy.conf import settings
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import reactor
from zijiyou.common.emailtool import sendMail
from zijiyou.db.mongoDbApt import MongoDbApt
import datetime
#from scrapy.core.scheduler import SchedulerpendingReqNum=len(Scheduler.pending_requests)
        

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
        
        self.mailInterval = None    #发送邮件间隔
        self.subject = "爬虫诊断信息" #邮件主题
        self.spiderName = None
        #发送邮件的时间间隔
        self.mailInterval=settings.get('MAIL_INTERVAL', None)
        #若有该邮件发送时间间隔配置信息，则进行定时发送诊断信息
        if self.mailInterval:
            reactor.callLater(self.mailInterval, self.onSendMail)
        
        #回调函数声明未知
#        dispatcher.connect(self.onResponseReceived,signal=signals.response_received)
        dispatcher.connect(self.onSpiderClose,signal=signals.spider_closed)
        dispatcher.connect(self.onSpiderOpen,signal=signals.spider_opened)
    
    def onSpiderOpen(self,spider):
        self.biginTime=datetime.datetime.now()
        self.spiderName = spider.name
        log.msg('爬虫：%s 扩展diagnoser：onSpiderOpen ' % spider.name,level=log.INFO)
                
    def onSpiderClose(self,spider):
        self.onSendMail(isClose=True)
    
    def onSendMail(self, isClose=False):
        content = self.getDiagnoseContent(isClose=isClose)
        log.msg("邮件内容 %s" %content , level=log.INFO)
        sendSucess = sendMail(self.subject, content)
        if sendSucess:
            log.msg("诊断邮件发送成功 %s" %datetime.datetime.now() , level=log.INFO)
            print "诊断邮件发送成功%s" %datetime.datetime.now()
            if not isClose:
                reactor.callLater(self.mailInterval, self.onSendMail)
        else:
            print "诊断邮件发送失败%s" %datetime.datetime.now()
            log.msg("诊断邮件发送失败，请检查settings中的email配置信息", level=log.ERROR)
            
    def getDiagnoseContent(self, isClose=False):
        content = ""
        if isClose:
            content = "爬虫结束时邮件诊断信息"
            endTime=datetime.datetime.now()
            intervalTemp=endTime - self.biginTime
            interval=intervalTemp.seconds
            if interval<self.thresholdRuntime:
                msg = "爬虫：%s 扩展diagnoser警告：错误-运行时间小于阀值。运行时间：%s秒，间隔阀值：%s秒" % (self.spiderName,interval,self.thresholdRuntime)
                content += "\r\n" + msg
                log.msg(msg, level=log.ERROR)
            elif (interval + 100) < self.closeSpiderTimeout:
                msg = "爬虫：%s 扩展diagnoser警告：运行时间小于setting的时间间隔。运行时间：%s秒，setting的时间间隔：%s秒" % (self.spiderName,interval,self.closeSpiderTimeout)
                content += "\r\n" + msg
                log.msg(msg, level=log.WARNING)
        else:
            content = "运行时邮件诊断信息"
        
        whereJson={'status':{'$gte':400}}
        untouchedUrlNum=self.mongo.countByWhere(self.crawlCol, whereJson)
        msg = "爬虫：%s 扩展diagnoser信息：剩余待爬取的网页数量：%s" % (self.spiderName,untouchedUrlNum)
        content += "\r\n" + msg
        log.msg(msg, level=log.INFO)
        if untouchedUrlNum<self.thresholdUntouchedUrl:
            msg = "爬虫：%s 扩展diagnoser警告：错误-剩余待爬取的网页数量低于阀值：%s" % (self.spiderName,untouchedUrlNum)
            content += "\r\n" + msg
            log.msg(msg, level=log.ERROR)
        
        return content
    
#    def onResponseReceived(self,response,request,spider):
#        if response.status in self.errorStatus:
#            self.errorCounter+=1
#        if self.errorCounter>self.thresholdError:
#            log.msg("扩展diagnoser警告：错误-某些错误出现次数大于阀值：%s" % self.errorCounter, level=log.ERROR)
#        log.msg('扩展diagnoser:onResponseReceived %s,%s' % (spider.name,self.errorCounter), level=log.INFO)
            