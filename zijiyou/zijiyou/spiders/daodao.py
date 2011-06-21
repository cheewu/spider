# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class Daodao(BaseCrawlSpider):
    '''
    Spider for www.daodao.com
    '''
    print '启动爬虫：daodaoSpider'
    log.msg('启动爬虫：daodaoSpider', level=log.INFO)
    name ="daodaoSpider"
    
#    def __init__(self,*a,**kw):
#        super(Daodao,self).__init__(*a,**kw)
#        self.initRequest()
        
SPIDER = Daodao()