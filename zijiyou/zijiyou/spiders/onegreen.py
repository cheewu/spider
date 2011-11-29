#coding:utf-8
'''
Created on 2011-11-29

@author: shiym
'''

from zijiyou.spiders.baseCrawlSpider import BaseCrawlSpider
class Onegreen(BaseCrawlSpider):
    '''
    下载onegreen的旅游地图
    '''
    name = "onegreenSpider"
    #指示是否需要马上解析item
    needParse = True
    
SPIDER = Onegreen()
    
        