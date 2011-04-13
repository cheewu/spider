# -*- coding: utf-8 -*-
'''
项目
Created on 2011-3-28
@author: shiym
'''

from scrapy.item import Item, Field

'''景点元数据结构'''
class ZijiyouItem(Item):
    '''
    struct information
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
 
'''完整的抓取页面结构'''   
class ContentItem(Item):
    '''
    classdocs
    '''
    pageUrl = Field()
    title = Field()
    content = Field()
    type = Field()
    
    def __str__(self):
        return ''

'''游记元数据结构'''  
class NoteItem(Item):
    title = Field()
    area = Field()
    type = Field()
    tag = Field()
    content = Field()
    date = Field()
    pageUrl = Field()
    
     
