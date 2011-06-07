# encoding:utf-8
'''
Created on 2011-6-6

@author: shiym
'''
from scrapy import log
from scrapy.utils.url import canonicalize_url
import datetime
import hashlib
import re

def getFingerPrint(inputs=[],isUrl=False):
    '''
    获得输入的指纹
    '''
    newInputs=[]
    if isUrl:
        for p in inputs:
            newInputs.append(canonicalize_url(p))
    else:
        newInputs=inputs
    
    if len(newInputs)<1:
        return 0; 
    hasher=hashlib.md5(newInputs[0])
    if len(newInputs)<2:
        return hasher.hexdigest()
    for index in range(1,len(newInputs)):
        input=newInputs[index]
        hasher.update(input)
    fp=hasher.hexdigest()
    return fp

class TxtDuplicateFilter(object):
    '''
    文本排重
    '''
    def __init__(self,md5Vals=[]):
        self.md5s=set()
        self.delimeters='[，。：；？！……\r\n]'
        if len(md5Vals)<1:
            print '初始化没有提供初始的md5值集合'
#            log.msg('初始化没有提供初始的md5值集合', level=log.WARNING)
        for p in md5Vals:
            self.md5s.add(p)
        
    def getKey(self,input):
        length = len(unicode(input))
        return length
    
    def getTopSentences(self,content='',topNum=10):
        '''
        获得长度最长的10个句子
        '''
        content=re.sub(unicode(self.delimeters), unicode(','), unicode(content))
        topSegments=[];
        segmentList=content.split(',');
        segmentList = sorted(segmentList,key=self.getKey,reverse=True)
        for segment in segmentList:
            topSegments.append(segment)
            topNum-=1
            if topNum<=0:
                break
        return topSegments
    
    def checkDuplicate(self,id=None,content=''):
        '''
        检测重复，若重复，返回true,重复的md5值，否则返回false，输入的md5值
        id：输入文本的id
        '''
        dt1=datetime.datetime.now()
        input=self.getTopSentences(content, topNum=10)
        md5Val=getFingerPrint(input);
        dt2=datetime.datetime.now()
        dt=dt2-dt1
        print '一次文本排重时间花费：%s' % dt
        
        if md5Val in self.md5s:
            print 'duplicate id为“%s”的输入被确定与md5Vale为“%s”的现有项目重复' % (id,md5Val)
#            log.msg('duplicate id为“%s”的输入被确定与md5Vale为“%s”的现有项目重复' % (id,md5Val),level=log.INFO)
            return True,md5Val
        else:
            self.md5s.add(md5Val)
            return False,md5Val

#测试
#if __name__ == "__main__":
#    dup=TxtDuplicateFilter()
#    isDup,md5Val=dup.checkDuplicate(id='110', content='测试，很好的，我的天哪')
#    print isDup
#    print md5Val