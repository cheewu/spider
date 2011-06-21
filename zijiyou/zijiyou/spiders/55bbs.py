# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class BBS55(BaseCrawlSpider):
    '''
    Spider for 55bbs.com
    '''
    print '55bbsSpider'
    log.msg('55bbsSpider', level=log.INFO)
    name ="55BBSSpider"
    
#    def __init__(self,*a,**kw):
#        super(BBS55,self).__init__(*a,**kw)
#        self.initRequest()
        
SPIDER = BBS55()

