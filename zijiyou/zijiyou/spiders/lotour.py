# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class lotour(BaseCrawlSpider):
    '''
    Spider for lotour.com
    '''
    print '�������棺lotourSpider'
    log.msg('�������棺loturSpider', level=log.INFO)
    name ="lotourSpider"
    
    def __init__(self,*a,**kw):
        super(lotour,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER = lotour()