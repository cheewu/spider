# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class t21cn(BaseCrawlSpider):
    '''
    Spider for 21cn.com
    '''
    print '∆Ù∂Ø≈¿≥Ê£∫21cnSpider'
    log.msg('∆Ù∂Ø≈¿≥Ê£∫21cnSpider', level=log.INFO)
    name ="21cnSpider"
    
    def __init__(self,*a,**kw):
        super(t21cn,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER =t21cn()
