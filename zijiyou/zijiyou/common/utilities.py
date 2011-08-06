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
from scrapy.exceptions import NotConfigured
from zijiyou.db.mongoDbApt import MongoDbApt

def getFingerPrint(inputs=[],isUrl=False):
    '''
    获得输入的指纹
    '''
    newInputs=[]
    if isUrl:
        for p in inputs:
            newP = canonicalize_url(p)
            tokens=newP.split('?')
            newTokens=[]
            if len(tokens) == 2:
                newTokens.append(tokens[0])
                temps=tokens[1].split('&')
                if len(temps)>1:
                    newTokens.extend(temps)
                else:
                    newTokens.extend(temps)
                    log.msg('%s ?后面的url只有一个参数' % p, level=log.DEBUG) 
            else:
                newTokens.extend(tokens)
                log.msg('%s url没有参数' % p, level=log.DEBUG)
                
            newInputs.extend(newTokens)
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
    def __init__(self,md5Vals=[],md5SourceCols=[]):
        self.md5s=set()
        self.delimeters='[，。：；？！……\r\n]'
        if len(md5Vals)>1:
            for p in md5Vals:
                self.md5s.add(p)
            print '完成文本排重器的md5初始化，共%s个md5值' % len(md5Vals)
        elif len(md5SourceCols) > 0:
            #从数据库加载md5
            mongoApt=MongoDbApt()
            for colName in md5SourceCols:
                cursor=mongoApt.findCursor(colName=colName, whereJson={'status':{'$gt':0},'isDup':False}, fieldsJson={'md5':1})
                for p in cursor:
                    if 'md5' in p:
                        self.md5s.add(p['md5'])
            print '完成文本排重器的md5初始化，共%s个md5值' % len(self.md5s)
        else:
            print '警告： 没有提供md5初始列表或md5数据源表，无法初始化文本排重器！'
#            raise NotConfigured
        if len(self.md5s)<1:
            print '初始化md5值集合为空！'
        
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
#        dt1=datetime.datetime.now()
        input=self.getTopSentences(content, topNum=10)
        md5Val=getFingerPrint(input)
#        dt2=datetime.datetime.now()
#        dt=dt2-dt1
#        print '一次文本排重时间花费：%s' % dt
        
        if md5Val in self.md5s:
#            log.msg('duplicate id为“%s”的输入被确定与md5Vale为“%s”的现有项目重复' % (id,md5Val),level=log.INFO)
            return True,md5Val
        else:
            self.md5s.add(md5Val)
            return False,md5Val

class ProcessBar(object):
    '''
    进度条
    '''
    def __init__(self,numAll=0,numUnit=1000):
        if numAll < 1:
            raise NotConfigured('总数量小于1，无法使用进度条！')
        self.numAll=numAll
        self.thredhold=self.numAll / numUnit
        self.percents=0.0
        self.curNum=0
        self.minUnit= 100.0 / numUnit
    
    def printProcessBar(self):
        '''
        打印进度
        '''
        self.curNum+=1
        if self.curNum >self.thredhold:
            self.percents += self.minUnit
            self.curNum=0
            print '当前进度：百分之%s' % self.percents
        
        

#测试 供理解代码参考
#if __name__ == "__main__":
#    dup=TxtDuplicateFilter()
#    isDup,md5Val=dup.checkDuplicate(id='110', content='测试，很好的，我的天哪')
#    print isDup
#    print md5Val
