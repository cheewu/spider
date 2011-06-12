# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class meishi(BaseCrawlSpider):
    '''
    Spider for meishiditu.com
    '''
    print '∆Ù∂Ø≈¿≥Ê£∫meishiSpider'
    log.msg('∆Ù∂Ø≈¿≥Ê£∫meishiSpider', level=log.INFO)
    name ="meishiSpider"
    
    def __init__(self,*a,**kw):
        super(meishi,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER =meishi()