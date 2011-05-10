# -*- coding: utf-8 -*-
'''
结构化数据
Created on 2011-3-28
@author: shiym
'''

from scrapy.item import Field, DictItem, Item
from zijiyou.items.baseItem import BaseItem

class ResponseBody(BaseItem):
    '''
    Content of Target page. the content field represent the boy of a response
    '''
    collectionName="ResponseBody"
    
    spiderName=Field()
    type = Field() # indicate the type of target page. such as note attractions... and so on
    pageUrl = Field()
    content = Field()
    dateTime=Field()
    
    reference=Field() #来源url
    
    def __str__(self):
        return 'ResponseBodyItem'

class Attraction(BaseItem):
    '''
    景点元数据结构
    '''
    collectionName="Attraction"
    
    area=Field()
    name=Field()
    englishName=Field()#景点英文名
    address=Field()
    photos=Field()
    desc=Field()        # description of the attraction
    descLink=Field()
    popularity=Field() #人气
    pageUrl=Field()    
    telNum=Field()     #电话
    
    openTime=Field()   #开放时间
    ticket=Field()     #票价
    type=Field()       #景点类型
    webAddress=Field() #网址
    replyNum = Field() #点评数
    center=Field()  #坐标
        
    def __str__(self):
        return "AttractionItem"
    
class Note(BaseItem):
    '''
    游记攻略
    '''  
    collectionName="Note"
    
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
    originUrl = Field()
    
    pvNum = Field()          #浏览量
    replyNum = Field()       #回复
    collectionNum = Field()  #收藏
    helpfulNum = Field()     #有用
    unhelpfulNum = Field()   #没有用
    
    honors = Field()         #荣誉 ， 如：原创、加精
    keyWords = Field()       #关键字  
    destination=Field() #旅游目的地
    
    def __str__(self):
        return "NoteItem"
    
class CommonSense(BaseItem):
    '''
    常识。如气候、文化等
    '''  
    collectionName="CommonSense"
    
    area = Field()
    author = Field()
    type = Field()
    content = Field()
    date = Field()
    pageUrl = Field()
    source = Field()         #来源：网页；用户输入；长文本
    
    pvNum = Field()          #浏览量
    replyNum = Field()       #回复
    collectionNum = Field()  #收藏
    helpfulNum = Field()     #有用
    unhelpfulNum = Field()   #没有用

    def __str__(self):
        return "CommonSenseItem"
    
class MemberInfo(BaseItem):
    '''
    会员主页信息
    '''
    collectionName="MemberInfo"
    
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

    def __str__(self):
        return "MemberInfo"

class MemberTrack(BaseItem):
    '''
    会员足迹
    '''
    collectionName="MemberTrack"
    
    pageUrl = Field()    
    name=Field()
    gone=Field()
    know=Field()
    like=Field()
    plan=Field()

    def __str__(self):
        return "MemberTrack"

class MemberFriend(BaseItem):
    '''
    会员好友
    '''
    collectionName="MemberFriend"
    
    pageUrl = Field()    
    #friends=Field() # like {friendName:address,friendName:address}
    name=Field()
    nameList = Field()
    cityList = Field()
    linkList = Field()
#    goneNumList = Field()
#    discoverList = Field()

    def __str__(self):
        return "MemberFriend"

class MemberNoteList(BaseItem):
    '''
    会员游记
    '''
    collectionName="MemberNoteList"
    
    pageUrl = Field()
    
    author = Field()
    titleList = Field()
    dateList = Field()
    
    pvNumList = Field()     #浏览量
    replyNumList = Field()  #回复    
    destinationList=Field() #旅游目的地

    def __str__(self):
        return "MemberNoteList"
    
class CityAttraction(BaseItem):
    name=Field()
    area=Field()
    introduction=Field()
    hotHotelLink=Field()
    
    def __str__(self):
        return "CityAttraction"
    
class CrawlUrl(BaseItem):
    '''
    CrawlDB
    '''
    collectionName="CrawlUrl"
    
    spiderName=Field()
    url=Field()
    callBack=Field() # the name of CallBackFunction Method Object
    priority=Field() # type is int
    dateTime=Field() # initiated by middleWare who save it to DB
    

    def __str__(self):
        return "CrawlUrl"
    
class KeyWord(Item):
    '''
    搜索引擎关键字
    '''
    collectionName="KeyWord"
    keyWord=Field()
    type=Field() #关键字搜索出的item类别。必须是现有item之一，否则无法存储。 与ResponseBody的type相同
    priority=Field() #关键字优先级
    
    seDate=Field()#最后一次搜索时间