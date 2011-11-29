# coding:utf-8
'''
Created on 2011-11-28

@author: shiym
'''
from scrapy import log
from scrapy.conf import settings
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider

class BaseCrawlSpider4Jinghua(BaseCrawlSpider):
    '''
    精华帖子
    '''
    def getPendingRequest(self):
        '''
        爬虫恢复初始化pendingRequest下载请求。只加载列表页
        '''
        #查询recent requests
        pendingRequest=[]
        #调度-10% 为下载异常
        cursor = self.apt.findPendingUrls4JinghuaByStatusAndSpiderName(self.name)
        num = self.urlIncreasement
        pendingRequest.extend(self.getRequestsFromCursor(cursor, num))
        num = len(pendingRequest)
        #重置下载计数器
        self.pendingRequestCounter = settings.get('PENDING_REQUEST_COUNTER')
        if self.pendingRequestCounter > len(pendingRequest):
            self.pendingRequestCounter = len(pendingRequest) - 20
        print "爬虫%s url补充总数：%s" % (self.name,len(pendingRequest))
        log.msg("爬虫%s url补充总数：%s" % (self.name,len(pendingRequest)),level=log.INFO)
        return pendingRequest