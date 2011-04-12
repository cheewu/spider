# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from scrapy.conf import settings

class RequestedUrlUpdate(object):
    '''
    访问过的url更新数据库
    '''
    def method(self):
        '''
        what is the proper name of method?
        '''
        pass
 

   
class RandomHttpProxy(object):
    proxyNum  = -1
    curProxyIndex = 0
    proxies = []

    def process_request(self, request, spider):
        '''init proxy configure'''
        if(self.proxyNum == -1):
            self.proxies = settings['PROXY']
            #print self.proxies
            self.proxyNum = len(self.proxies)
            
        if(self.proxyNum != 0):
            request.meta['proxy'] = self.proxies[self.curProxyIndex]
            self.curProxyIndex = (self.curProxyIndex + 1) % self.proxyNum
