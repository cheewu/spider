# -*- coding: utf-8 -*-
'''
Created on 2011-3-28
@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class bytravel(BaseCrawlSpider):
    '''
    Spider for bytravel.cn
    '''
    print '�������棺bytravelSpider'
    log.msg('�������棺bytravelSpider', level=log.INFO)
    name ="bytravelSpider"
    
    def __init__(self,*a,**kw):
        super(bytravel,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER =bytravel()