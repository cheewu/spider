# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class lvren(BaseCrawlSpider):
    '''
    Spider for lvren.cn
    '''
    print '�������棺lvrenSpider'
    log.msg('�������棺lvrenSpider', level=log.INFO)
    name ="lvrenSpider"
    
    def __init__(self,*a,**kw):
        super(lvren,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER =lvren()