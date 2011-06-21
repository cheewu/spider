# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class lvyou114(BaseCrawlSpider):
    '''
    Spider for www.lvyou114.com
    '''
    print 'lvyou114Spider'
    log.msg('lvyou114Spider', level=log.INFO)
    name ="lvyou114Spider"
    
#    def __init__(self,*a,**kw):
#        super(lvyou114,self).__init__(*a,**kw)
#        self.initRequest()
        
SPIDER =lvyou114()