# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class sohu(BaseCrawlSpider):
    '''
    Spider for travel.sohu.com
    '''
    print '�������棺sohuSpider'
    log.msg('�������棺sohuSpider', level=log.INFO)
    name ="sohuSpider"
    
    def __init__(self,*a,**kw):
        super(sohu,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER = sohu()