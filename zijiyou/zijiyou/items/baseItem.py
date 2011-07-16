# -*- coding: utf-8 -*-
'''
Created on 2011-4-26

@author: shiym
'''
from scrapy.item import Item, Field

class BaseItem(Item):
    '''
    结构化信息父类，包含了子类必须有的字段
    '''
    status=Field()     # log the operation. default is 100, indicates initial status
    pushDateTime=Field()    #最近一次推送日期
    spiderName=Field()      #爬虫名
    url=Field()             #来源网页链接

#    def __str__(self):
#        return "BaseItem"

    def __init__(self,*kw):
        super(BaseItem, self).__init__(*kw)
        self['status']=100