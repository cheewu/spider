# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from zijiyou.spiders.baseBBSSpider import BaseBBSSpider
class BBS55(BaseBBSSpider):
    '''
    Spider for 55bbs.com
    '''
    print '55bbsSpider'
    log.msg('55bbsSpider', level=log.INFO)
    name ="55bbsSpider"
    
SPIDER = BBS55()
