# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class yiqiyou(BaseCrawlSpider):
    '''
    Spider for www.17u.com
    '''
    print '�������棺17uSpider'
    log.msg('�������棺17uSpider', level=log.INFO)
    name ="17uSpider"
    
    def __init__(self,*a,**kw):
        super(yiqiyou,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER = yiqiyou()