# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class people(BaseCrawlSpider):
    '''
    Spider for travel.people.com
    '''
    print '�������棺peopleSpider'
    log.msg('�������棺peopleSpider', level=log.INFO)
    name ="peopleSpider"
    
    def __init__(self,*a,**kw):
        super(people,self).__init__(*a,**kw)
        self.initRequest()
        
SPIDER =people()