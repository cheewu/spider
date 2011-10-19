# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class Lvping(BaseCrawlSpider):
    '''
    Spider for www.lvping.com
    '''
    name ="lvpingSpider"
    download_delay = 3
    
SPIDER = Lvping()