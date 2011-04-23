# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class Lvping(BaseCrawlSpider):
    '''
    Spider for www.daodao.com
    '''
    print '启动爬虫：lvpingSpider'
    log.msg('启动爬虫：lvpingSpider', level=log.INFO)
    name ="lvpingSpider"
    
SPIDER = Lvping()