# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
from scrapy import log
from zijiyou.spiders.baseBBSSpider import BaseBBSSpider
class lvren(BaseBBSSpider):
    '''
    Spider for lvren.cn
    '''
    print '55bbsSpider'
    log.msg('55bbsSpider', level=log.INFO)
    name ="55bbsSpider"
    
#    def __init__(self,*a,**kw):
#        super(lvren,self).__init__(*a,**kw)
#        self.initRequest()
        
SPIDER =lvren()
