# -*- coding: utf-8 -*-
'''
Created on 2011-5-4

@author: shiym
'''
from scrapy import log, signals
from scrapy.conf import settings
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import reactor
#from zijiyou.common.emailTool import sendMail
from scrapy.mail import MailSender
from zijiyou.db.mongoDbApt import MongoDbApt
from collections import defaultdict
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
        self.crawlCol='UrlDb'
        #发送邮件的时间间隔
        self.mailInterval=settings.get('MAIL_INTERVAL', None)
        #爬虫系统速度
        self.pagecounts = defaultdict(int)
        self.totalPagecounts = 0
        #若有该邮件发送时间间隔配置信息，则进行定时发送诊断信息
        if self.mailInterval:
            self.mailer=MailSender()
            self.mailTos=settings.get('MAIL_TO_LIST')
            reactor.callLater(self.mailInterval, self.onSendMail)
        
        #回调函数声明未知
        dispatcher.connect(self.onSpiderClose,signal=signals.spider_closed)
        dispatcher.connect(self.onSpiderOpen,signal=signals.spider_opened)
        dispatcher.connect(self.onResponseReceived, signal=signals.response_received)
    
    def onSpiderOpen(self,spider):
        self.biginTime=datetime.datetime.now()
        log.msg('爬虫：%s 扩展diagnoser：onSpiderOpen ' % spider.name,level=log.INFO)
                
    def onSpiderClose(self,spider):
        self.onSendMail(isClose=True)
    
    def onSendMail(self, isClose=False):
        content = self.getDiagnoseContent(isClose=isClose)
        if not self.mailInterval:
            return
        log.msg("邮件内容 %s" %content , level=log.INFO)
        self.mailer.send(to=self.mailTos, subject='爬虫诊断信息', body=content);
        log.msg("诊断邮件发送完成 时间：%s，邮件内容：%s" % (datetime.datetime.now(),content) , level=log.INFO)
        #若关闭spider则不再发送邮件
        if not isClose:
            reactor.callLater(self.mailInterval, self.onSendMail)
            
    def getDiagnoseContent(self, isClose=False):
        content = ""
        if isClose:
            content = "爬虫结束时邮件诊断信息"
            endTime=datetime.datetime.now()
            intervalTemp=endTime - self.biginTime
            interval=intervalTemp.seconds
            log.msg('爬虫诊断 运行时间=%s秒' % (interval),level=log.INFO)
            if interval<self.thresholdRuntime:
                msg = "爬虫诊断 运行时间小于阀值。总运行时间：%s秒，间隔阀值：%s秒" % (interval,self.thresholdRuntime)
                content += "\r\n" + msg
                log.msg(msg, level=log.ERROR)
            elif (interval + 100) < self.closeSpiderTimeout:
                msg = "爬虫诊断 运行时间小于爬虫规定的运行时间间隔。运行时间：%s秒，setting的时间间隔：%s秒" % (interval,self.closeSpiderTimeout)
                content += "\r\n" + msg
                log.msg(msg, level=log.WARNING)
        else:
            content = "运行时邮件诊断信息"
        
        whereJson={'status':{'$gte':400,'$lt':900}}
        errorUrlNum=self.mongo.countByWhere(self.crawlCol, whereJson)
        if errorUrlNum>self.thresholdError:
            msg = "爬虫诊断 ：下载失败网页数量为%s，高于于阀值%s" % (errorUrlNum,self.thresholdError)
            content += "\r\n" + msg
        whereJson={'status':{'$gt':900}}
        untouchedUrlNum=self.mongo.countByWhere(self.crawlCol, whereJson)
        if untouchedUrlNum<self.thresholdUntouchedUrl:
            msg = "爬虫诊断 剩余待爬取的网页数量：%s，低于阀值%s" % (untouchedUrlNum,self.thresholdUntouchedUrl)
            content += "\r\n" + msg
        else:
            msg = "爬虫诊断 剩余待爬取的网页数量：%s" % (untouchedUrlNum)
            content += "\r\n" + msg
        #爬虫速度
        speed=self.totalPagecounts* 60.0 % self.mailInterval
        content += "\r\n最近%s小时内，下载网页总数为%s个，爬虫速度为:%s/分钟" % (self.mailInterval / 3600.0 ,self.totalPagecounts, speed) 
        #统计爬虫数
        spiderNames=self.pagecounts.keys()
        content += "\r\n最近%s小时内执行过的爬虫有：%s" % (self.mailInterval / 3600.0 , spiderNames)
        self.totalPagecounts=0
        self.pagecounts.clear()
        return content
    
    def onResponseReceived(self,response, request, spider):
        self.pagecounts[spider] += 1
        self.totalPagecounts += 1
        