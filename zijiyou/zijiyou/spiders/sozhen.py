# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class sozhen(BaseCrawlSpider):
    '''
    Spider for lvren.cn
    '''
    print '∆Ù∂Ø≈¿≥Ê£∫lvrenSpider'
    log.msg('∆Ù∂Ø≈¿≥Ê£∫lvrenSpider', level=log.INFO)
    name ="sozhenSpider"
    
    def __init__(self,*a,**kw):
        super(sozhen,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER =sozhen()
