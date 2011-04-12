# -*- coding: utf-8 -*-
'''
项目
Created on 2011-3-28
@author: shiym
'''

from scrapy.item import Item, Field

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
     
