# -*- coding: utf-8 -*-

import re
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose, Join
from scrapy.utils.markup import remove_entities

'''
define the methods to manage output

def encodeUft8(inputs):
    value = "-".join("%s" % p for p in inputs)
    print(value)
    return value.encode("utf-8")
'''
#print ('++itemlocader +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
textProcessor = Compose(TakeFirst(), remove_entities,Join())
joinProcessor = Compose(remove_entities,Join())

class ZijiyouItemLoader(XPathItemLoader):
    '''
    override the default_output_processor. 
    '''
    #default_output_processor = textProcessor
    #address_in = joinProcessor
