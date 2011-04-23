# -*- coding: utf-8 -*-
'''
结构化数据
Created on 2011-3-28
@author: shiym
'''

from scrapy.item import Item, Field, DictItem

class ResponseBody(Item):
    '''
    Content of Target page. the content field represent the boy of a response
    '''
    spiderName=Field()
    type = Field() # indicate the type of target page. such as note attractions... and so on
    pageUrl = Field()
    content = Field()
    status=Field()     # log the operation. default is 100, indicates initial status
    dateTime=Field()
    
    def __str__(self):
        return 'ResponseBodyItem'

class Attraction(Item):
    '''
    景点元数据结构
    '''
    area=Field()
    name=Field()
    address=Field()
    photos=Field()
    desc=Field()        # description of the attraction
    descLink=Field()
    popularity=Field() #人气
    pageUrl=Field()    
    telNum=Field()     #电话
    
    openTime=Field()   #开发时间
    ticket=Field()     #票价
    type=Field()       #景点类型
    webAddress=Field() #网址
    replyNum = Field() #点评数
    
    status=Field()      # log the operation. default is 100, indicates initial status
    pushDate=Field()    #最近一次推送日期
        
    def __str__(self):
        return "AttractionItem"

class Note(Item):
    '''
    游记攻略
    '''  
    title = Field()
    author = Field()
    area = Field()
    type = Field()         #游记分类
    tag = Field()          #标签
    attractions = Field()  #沿途风景
    feature = Field()      #线路特色
    content = Field()
    date = Field()
    pageUrl = Field()
    
    pvNum = Field()          #浏览量
    replyNum = Field()       #回复
    collectionNum = Field()  #收藏
    helpfulNum = Field()     #有用
    unhelpfulNum = Field()   #没有用
    
    honors = Field()         #荣誉 ， 如：原创、加精
    keyWords = Field()       #关键字  
    destination=Field() #旅游目的地
    
    status=Field()      # log the operation. default is 100, indicates initial status
    pushDate=Field()    #最近一次推送日期
    
    def __str__(self):
        return "NoteItem"
    
class CommonSense(Item):
    '''
    常识。如气候、文化等
    '''  
    area = Field()
    author = Field()
    type = Field()
    content = Field()
    date = Field()
    pageUrl = Field()
    
    pvNum = Field()          #浏览量
    replyNum = Field()       #回复
    collectionNum = Field()  #收藏
    helpfulNum = Field()     #有用
    unhelpfulNum = Field()   #没有用
    status=Field()     # log the operation. default is 100, indicates initial status
    pushDate=Field()    #最近一次推送日期

    def __str__(self):
        return "CommonSenseItem"
    
class MemberInfo(Item):
    '''
    会员主页信息
    '''
    pageUrl = Field()    
    name=Field() 
    currentAddress=Field() #现居
    selfIntroduction=Field() #自我介绍
    comsumptionLevel=Field() #通常的旅行花费
    travalPurpose=Field() #大部分时候旅行是为了
    ageRange=Field() #年龄段
    gender=Field() #性别
    travelPreference=Field() #度假偏好
    travelPartner=Field() #通常和谁旅行
    
    status=Field()     # log the operation. default is 100, indicates initial status
    pushDate=Field()    #最近一次推送日期

    def __str__(self):
        return "MemberInfo"

class MemberTrack(Item):
    '''
    会员足迹
    '''
    pageUrl = Field()    
    name=Field()
    track=Field() # like {friendName:address,friendName:address}
    
    status=Field()     # log the operation. default is 100, indicates initial status
    pushDate=Field()    #最近一次推送日期

    def __str__(self):
        return "MemberTrack"

class MemberFriend(Item):
    '''
    会员好友
    '''
    pageUrl = Field()    
    friends=Field() # like {friendName:address,friendName:address}
    
    status=Field()     # log the operation. default is 100, indicates initial status
    pushDate=Field()    #最近一次推送日期

    def __str__(self):
        return "MemberFriend"

class MemberNoteList(Item):
    '''
    会员游记
    '''
    pageUrl = Field()
    
    title = Field()
    author = Field()
    date = Field()
    
    pvNum = Field()     #浏览量
    replyNum = Field()  #回复    
    destination=Field() #旅游目的地
    
    status=Field()     # log the operation. default is 100, indicates initial status
    pushDate=Field()   #最近一次推送日期

    def __str__(self):
        return "MemberNoteList"
    
class CrawlUrl(Item):
    '''
    CrawlDB
    '''
    spiderName=Field()
    url=Field()
    callBack=Field() # the name of CallBackFunction Method Object
    status=Field()   # http status code , type is int
    priority=Field() # type is int
    dateTime=Field() # initiated by middleWare who save it to DB
    
    status=Field()     # log the operation. default is 100, indicates initial status
    pushDate=Field()   #最近一次推送日期

    def __str__(self):
        return "CrawlUrl"
    