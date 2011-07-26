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
    name ="sohuSpider"
        
SPIDER = sohu()