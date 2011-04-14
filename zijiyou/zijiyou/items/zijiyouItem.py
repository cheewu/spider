# -*- coding: utf-8 -*-
'''
项目
Created on 2011-3-28
@author: shiym
'''

from scrapy.item import Item, Field

class ZijiyouItem(Item):
    '''
    景点元数据结构
    '''
    area=Field()
    name=Field()
    address=Field()
    photos=Field()
    desc=Field() # description of the attraction
    descLink=Field()
    popularity=Field()
    pageUrl=Field()
    telNum=Field()
    #travelerReviews={}
    
    def __str__(self):
        return "ZijiyouItem"

class ContentItem(Item):
    '''
    classdocs
    '''
    pageUrl = Field()
    title = Field()
    content = Field()
    type = Field()
    
    def __str__(self):
        return 'ContentItem'


class NoteItem(Item):
    '''
    游记元数据结构
    '''  
    title = Field()
    area = Field()
    type = Field()
    tag = Field()
    content = Field()
    date = Field()
    pageUrl = Field()
      
    def __str__(self):
        return "NoteItem"
