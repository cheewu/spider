# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class Sina(BaseCrawlSpider):
    '''
    Spider for sina.com
    '''
    print '�������棺sinaSpider'
    log.msg('�������棺sinaSpider', level=log.INFO)
    name ="sinaSpider"
    
    def __init__(self,*a,**kw):
        super(Sina,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER = Sina()