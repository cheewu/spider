# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class hexun(BaseCrawlSpider):
    '''
    Spider for travel.hexun.com
    '''
    print '∆Ù∂Ø≈¿≥Ê£∫hexunSpider'
    log.msg('∆Ù∂Ø≈¿≥Ê£∫hexunSpider', level=log.INFO)
    name ="hexunSpider"
    
    def __init__(self,*a,**kw):
        super(hexun,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER =hexun()