# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from scrapy.conf import settings

class RequestSaver(object):
    '''
    重新开始crawl 
    '''
    
    def enqueue_request(self,spider,request):
        spider.recent_requests.append(request.url)
        while len(spider.recent_requests) > settings.get('RECENT_URLS_SIZE',300):
            spider.recent_requests.pop(0)
        return None
    