# -*- coding: utf-8 -*-
'''
Created on 2011-4-26

@author: shiym
'''
from scrapy.item import Item, Field

class BaseItem(Item):
    '''
    结构化信息父类
    '''
    status=100     # log the operation. default is 100, indicates initial status
    pushDate=Field()   #最近一次推送日期
    spiderName=Field() #爬虫名
    

        
