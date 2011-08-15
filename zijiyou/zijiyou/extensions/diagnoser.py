# -*- coding: utf-8 -*-
'''
Created on 2011-5-4

@author: shiym
'''
from collections import defaultdict
from scrapy import log, signals
from scrapy.conf import settings
from scrapy.http import Response
from scrapy.mail import MailSender
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import reactor
from zijiyou.db.extensionApt import DiagnoserApt
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
        #诊断器的适配器
        self.apt = DiagnoserApt()
        #发送邮件的时间间隔
        self.mailInterval=settings.get('MAIL_INTERVAL', 14400)
        #发送邮件最小间隔
        self.minMailInterval=settings.get('MIN_MAIL_INTERVAL', 30)
        #爬虫系统速度
        self.totalPagecounts = 0
        self.dtBegin=datetime.datetime.now()
        #若有该邮件发送时间间隔配置信息，则进行定时发送诊断信息
        if self.mailInterval:
            self.mail=settings.get('MAIL')
            self.mailer=MailSender()
            self.mailTos=settings.get('MAIL_TO_LIST')
            reactor.callLater(self.mailInterval, self.onSendMail)
        #爬虫字典
        self.spiderDict={}
        #错误的crawl状态
        self.faildedStatus=[400,403,404]
        #回调函数声明未知
        dispatcher.connect(self.onSpiderClose,signal=signals.spider_closed)
        dispatcher.connect(self.onSpiderOpen,signal=signals.spider_opened)
        dispatcher.connect(self.onResponseReceived, signal=signals.response_received)
    
    def onSpiderOpen(self,spider):
        self.beginTime=datetime.datetime.now()#可能要改
        log.msg('diagonoser： 爬虫%s开始运行' % spider.name,level=log.INFO)
        spiderName=spider.name
        if not spiderName:
            log.msg('diagonoser发现没有名字的爬虫：%s' % spider,level=log.ERROR)
            return
        self.spiderDict[spiderName] = {
                                         'beginTime':datetime.datetime.now(), #爬虫开启时间
                                         'crawledCounter':0, #下载网页数
                                         'faildedCounter':defaultdict(int), #失败网页数={失败的code：数量}
                                        }
                
    def onSpiderClose(self,spider,reason):
        log.msg('爬虫%s关闭，关闭原因：%s' % (spider.name,reason),level=log.INFO)
        self.onSendMail(isClose=True,spiderName=spider.name,closedReason=reason)
        if spider.name in self.spiderDict:
            self.spiderDict.pop(spider.name)
        else:
            log.msg('diagonoser：爬虫%s关闭时发现其没有记录在spiderDict中！' % spider.name,level=log.ERROR)
    
    def onSendMail(self, isClose=False,msg=None,spiderName='',closedReason=''):
        content = self.getDiagnoseContent(isClose=isClose,spiderName=spiderName,closedReason=closedReason)
        log.msg("邮件内容 %s" %content , level=log.INFO)
        #判断时间间隔
        dtNow=datetime.datetime.now()
        dtInterval=dtNow-self.beginTime
        self.beginTime=dtNow
        if dtInterval.seconds < self.minMailInterval:
            return
        
        if self.mail:
            self.mailer.send(to=self.mailTos, subject='爬虫诊断信息', body=content)
        #若关闭spider则不再发送邮件
        if not isClose:
            reactor.callLater(self.mailInterval, self.onSendMail)
            
    def getDiagnoseContent(self, isClose=False,spiderName='',closedReason=''):
        content = ""
        if isClose:
            content = "爬虫%s关闭。关闭原因：%s  " % (spiderName,closedReason) 
            endTime=datetime.datetime.now()
            intervalTemp=endTime - self.spiderDict[spiderName]['beginTime']
            interval=intervalTemp.seconds+1
            content += "总运行时间：%s秒  " % (interval)
            content += "下载网页总数：%s  " % self.spiderDict[spiderName]['crawledCounter']
            content +="速度：%s/分钟  \n" % (self.spiderDict[spiderName]['crawledCounter'] * 60.0 / interval )
            content +="下载失败网页数信息：%s\n" % (self.spiderDict[spiderName]['faildedCounter'])
            #清除爬虫
            self.spiderDict.pop(spiderName)
        else:
            content = "运行时邮件诊断信息\n"
        
        #收集每个爬虫的执行情况
        for key in self.spiderDict.keys():
            msg = "爬虫%s的诊断信息：" % key
            msg += "  下载网页总数：%s " % self.spiderDict[key]['crawledCounter']
            msg += "  速度：%s/分钟 " % (self.spiderDict[key]['crawledCounter'] * 60 / (datetime.datetime.now() - self.spiderDict[key]['beginTime']).seconds )
            self.spiderDict[key]['crawledCounter'] = 0
            self.spiderDict[key]['beginTime'] = datetime.datetime.now()
            msg += "  下载失败网页数信息：%s\n" % self.spiderDict[key]['faildedCounter']
            content +=msg

        #收集爬虫系统总体信息
        if self.totalPagecounts >10:
            interval=(datetime.datetime.now()-self.dtBegin).seconds + 1
            #总下载失败网页数量
            errorUrlNum=self.apt.countErrorStatusUrls()
            content += "爬虫系统总体状态：\n总下载失败网页数量为%s  " % errorUrlNum
            #总剩余待爬取的网页数量
            untouchedUrlNum=self.apt.countUncrawlUrls()
            content += "总剩余待爬取的网页数量：%s  \n" % (untouchedUrlNum)
            #爬虫总速度
            speed=self.totalPagecounts * 60.0 / interval
            content += "最近%s小时内，下载网页总数为%s个，总速度为:%s/分钟 " % (self.mailInterval / 3600.0 ,self.totalPagecounts, speed) 
            #统计爬虫数
            content += "爬虫队列：%s " % (self.spiderDict.keys())
            self.totalPagecounts=0
        
        return content
    
    def onResponseReceived(self,response, request, spider):
        '''
        下载一个网页
        '''
        self.totalPagecounts += 1
        self.spiderDict[spider.name]['crawledCounter'] += 1
        if isinstance(response,Response) and response.status in self.faildedStatus:
            self.spiderDict[spider.name]['faildedCounter'][response.status] += 1
