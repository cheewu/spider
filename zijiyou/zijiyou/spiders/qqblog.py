# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: shiym
'''
from scrapy import log
from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class QQBlog(BaseCrawlSpider):
    '''
    Spider for www.daodao.com
    '''
    print '启动爬虫：qqblogSpider'
    log.msg('启动爬虫：qqBlogSpider', level=log.INFO)
    name ="QQBlogSpider"
    
#    def __init__(self,*a,**kw):
#        super(QQBlog,self).__init__(*a,**kw)
#        self.initRequest()
        
SPIDER = QQBlog()

