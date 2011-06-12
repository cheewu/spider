# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class bbker(BaseCrawlSpider):
    '''
    Spider for www.bbker.com
    '''
    print '∆Ù∂Ø≈¿≥Ê£∫bbkerSpider'
    log.msg('∆Ù∂Ø≈¿≥Ê£∫bbkerSpider', level=log.INFO)
    name ="bbkerSpider"
    
    def __init__(self,*a,**kw):
        super(bbker,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER = bbker()