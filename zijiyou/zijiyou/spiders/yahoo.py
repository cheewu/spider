# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class yahoo(BaseCrawlSpider):
    '''
    Spider for travel.cn.yahoo.com
    '''
    print '∆Ù∂Ø≈¿≥Ê£∫yahooSpider'
    log.msg('∆Ù∂Ø≈¿≥Ê£∫yahooSpider', level=log.INFO)
    name ="yahooSpider"
    
    def __init__(self,*a,**kw):
        super(sozhen,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER =yahoo()