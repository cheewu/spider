# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: wuqi
'''
<<<<<<< HEAD
from scrapy import log
from zijiyou.spiders.baseBBSSpider import BaseBBSSpider
class lvren(BaseBBSSpider):
    '''
    Spider for lvren.cn
    '''
    print '55bbsSpider'
    log.msg('55bbsSpider', level=log.INFO)
    name ="55bbsSpider"
=======
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class lvren(BaseCrawlSpider):
    '''
    Spider for lvren.cn
    '''
    name ="lvrenSpider"
>>>>>>> 5a91f24ee3ddf31e7deaeeb309cf25dc7ad7a410
    
SPIDER =lvren()
