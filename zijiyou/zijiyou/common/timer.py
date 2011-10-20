# coding:utf-8
'''
Created on 2011-9-21

@author: shiym
'''
import threading
import time

class ZijiyouTimer(threading.Thread):
    """
    定时器
    """
    
    def __init__(self,seconds,action,parameter):
        self.seconds=seconds
        self.action=action
        self.parameter=parameter
        super(ZijiyouTimer,self).__init__()
        
    def run(self):
        """
        执行
        """
        time.sleep(self.seconds)
        if self.parameter:
            self.action(self.parameter)
        else:
            self.action()