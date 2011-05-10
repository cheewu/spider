# -*- coding: utf-8 -*-
'''
Created on 2011-5-10

@author: shiym
'''

import datetime
import os

class Loger(object):
    '''
    classdocs
    '''

    def __init__(self,logFileName):
        '''
        Constructor
        '''
        self.logFileName=logFileName
        if os.path.exists(logFileName):
            self.loger=open(logFileName,'a')
        else:
            self.loger=open(logFileName,'w')
        
    def log(self,msg,level):
        if not msg or not level or len(msg)<2:
            return
        self.loger.write('%s level=%s  :%s \n' %(datetime.datetime.now(),level,msg))
        
    def readLog(self):
        pass
        