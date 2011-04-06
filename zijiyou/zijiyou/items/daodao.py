# -*- coding: utf-8 -*-
'''
Created on 2011-3-28

@author: ibm
'''
from scrapy.item import Item,Field

class Daodao(Item):
    '''
    Item of DaodaoSite
    '''
    area=Field()
    name=Field()
    tags=Field()
    address=Field()
    telNum=Field()
    photos=Field()
    

    def __init__(self):
        '''
        Constructor
        '''
        