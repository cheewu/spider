'''
Created on 2011-4-8

@author: qiuqm
'''
from scrapy.item import Field, Item

class ContentItem(Item):
    '''
    classdocs
    '''
    pageUrl = Field()
    title = Field()
    content = Field()
    type = Field()
    
    def __str__(self):
        return "ContentItem"
        