# encoding:utf-8
'''
Created on 2011-6-2

@author: shiym
'''
import datetime
import hashlib
import re

md5s={}
delimeters='[，。：；？！……\r\n]'

def getFingerPrint(inputs=[]):
    '''
    指纹
    '''
    if len(inputs)<1:
        return 0; 
    hasher=hashlib.md5(inputs[0])
    for index in range(1,len(inputs)):
        input=inputs[index]
        hasher.update(input)
    fp=hasher.hexdigest()
    return fp

def getKey(input):
    length = len(unicode(input))
    return length

def getTopSentences(content='',topNum=10):
    '''
    获得长度最长的10个句子
    '''
    content=re.sub(unicode(delimeters), unicode(','), unicode(content))
    topSegments=[];
    segmentList=content.split(',');
    segmentList = sorted(segmentList,key=getKey,reverse=True)
    for segment in segmentList:
        topSegments.append(segment)
        topNum-=1
        if topNum<=0:
            break
    return topSegments

def checkDuplicate(id=None,content):
    '''
    检测重复，若重复，返回已存在的id，否则返回空
    '''
    dt1=datetime.datetime.now()
    input=getTopSentences(content, topNum=10)
    md5Val=getFingerPrint(input);
    dt2=datetime.datetime.now()
    dt=dt2-dt1
    print '时间代价：%s' % dt
    
    if md5Val in md5s:
        print 'duplicate key:%s,md5Vale:%s' %(id,md5Val)
        return md5s[md5Val]
    else:
        md5s[md5Val]=id
        return None
        