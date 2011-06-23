# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
<<<<<<< HEAD
from scrapy import log
from zijiyou.spiders.baseBBSSpider import BaseBBSSpider
class BBS55(BaseBBSSpider):
    '''
    Spider for 55bbs.com
    '''
    print '55bbsSpider'
    log.msg('55bbsSpider', level=log.INFO)
    name ="55bbsSpider"
=======
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class BBS55(BaseCrawlSpider):
    '''
    Spider for 55bbs.com
    '''
    name ="55BBSSpider"
>>>>>>> 5a91f24ee3ddf31e7deaeeb309cf25dc7ad7a410
    
SPIDER = BBS55()
