# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class mafengwo(BaseCrawlSpider):
    '''
    Spider for mafengwo.cn 
    '''
    print 'mafengwoSpider'
    log.msg('mafengwoSpider', level=log.INFO)
    name ="mafengwoSpider"
    
#    def __init__(self,*a,**kw):
#        super(mafengwo,self).__init__(*a,**kw)
#        self.initRequest()
        
SPIDER =mafengwo()