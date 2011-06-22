# -*- coding: utf-8 -*-
'''
结构化数据
Created on 2011-3-28
@author: shiym
'''

from scrapy.item import Field, Item
from zijiyou.items.baseItem import BaseItem
    
class UrlDb(BaseItem):
    '''
    CrawlDB
    '''
    collectionName=Field()
    
    reference=Field() #来源url
    callBack=Field() # the name of CallBackFunction Method Object
    priority=Field() # type is int
    dateTime=Field() # initiated by middleWare who save it to DB
    updateInterval=Field() #更新间隔

    def __str__(self):
        return "UrlDb"
    
    def __init__(self,*kw):
        super(UrlDb, self).__init__(*kw)
        self['collectionName']="UrlDb"
    
class PageDb(BaseItem):
    '''
    存储所有的page content，景点 景区 攻略 用户 个人页面
    '''
    collectionName = Field() 
    
    itemCollectionName = Field() # item表名
    responseBody = Field() 
    optDateTime=Field() #保存时间
    
    def __str__(self):
        return 'PageDbItem'
    
    def __init__(self,*kw):
        super(PageDb, self).__init__(*kw)
        self['collectionName']="PageDb"

class POI(BaseItem):
    '''
    所有的poi 包括 景点 景区 酒店 机场 火车站.. 
    '''
    collectionName=Field()
    
    area=Field()
    name=Field()
    englishName=Field()#景点英文名
    address=Field()
    photos=Field()
    desc=Field()        # description of the attraction
    descLink=Field()
    popularity=Field() #人气
    telNum=Field()     #电话
    
    openTime=Field()   #开放时间
    ticket=Field()     #票价
    traffic=Field()    #交通
    type=Field()       #POI类型
    webAddress=Field() #网址
    replyNum = Field() #点评数
    center=Field()  #坐标
        
    imageUrls = Field()     #图片原始链接列表
    imagesInfo = Field()   #图片信息，是一个2元组列表。eg：(True 图片是否有效, {'checksum':图片MD5值，用于排重，如 '2b00042f7481c7b056c4b410d28f33cf','path': 图片在本地的路径，如'full/7d97e98f8af710c7e7fe703abc8f639e0ee507c4.jpg','url': 原始地址，如'http://www.example.com/images/product1.jpg'})
        
    def __str__(self):
        return "POIItem"
    
    def __init__(self,*kw):
        super(POI, self).__init__(*kw)
        self['collectionName']="POI"
    
class Article(BaseItem):
    '''
    长文本，如游记 攻略
    '''  
    collectionName=Field() #表名
    
    title = Field()     #标题
    author = Field()    #作者
    area = Field()      #地区
    type = Field()         #文本类型
    tag = Field()          #标签
    attractions = Field()  #沿途风景
    feature = Field()      #线路特色
    content = Field()       #文章内容
    publishDate = Field()   #发表日期
    originUrl = Field()     #文章原始链接 用于搜索引擎爬虫的快照爬取
    abstract = Field()      #文章摘要
    
    pvNum = Field()          #浏览量
    replyNum = Field()       #回复
    collectionNum = Field()  #收藏
    helpfulNum = Field()     #有用
    unhelpfulNum = Field()   #没有用
    
    honors = Field()         #荣誉 ， 如：原创、加精
    keyWords = Field()       #关键字  
    destination=Field()      #旅游目的地
    
    imageUrls = Field()     #图片原始链接列表
    imagesInfo = Field()   #图片信息，是一个2元组列表。eg：(True 图片是否有效, {'checksum':图片MD5值，用于排重，如 '2b00042f7481c7b056c4b410d28f33cf','path': 图片在本地的路径，如'full/7d97e98f8af710c7e7fe703abc8f639e0ee507c4.jpg','url': 原始地址，如'http://www.example.com/images/product1.jpg'})
    
    md5=Field()             #MD5值
    
    def __str__(self):
        return "ArticleItem"
    
    def __init__(self,*kw):
        super(Article, self).__init__(*kw)
        self['collectionName']="Article"
        self['imageUrls']=[]
    
class Note(BaseItem):
    '''
    短文本 如常识 气候、文化等
    '''  
    collectionName=Field()
    
    area = Field()
    author = Field()
    noteType = Field()          #文本类型
    content = Field()
    publishDate = Field()   #发表日期
    source = Field()        #来源：网页；用户输入；长文本
    
    pvNum = Field()         #浏览量
    replyNum = Field()      #回复
    collectNum = Field()    #收藏
    helpfulNum = Field()    #有用
    unhelpfulNum = Field()  #没有用
    
    imageUrls = Field()     #图片原始链接列表
    imagesInfo = Field()   #图片信息，是一个2元组列表。eg：(True 图片是否有效, {'checksum':图片MD5值，用于排重，如 '2b00042f7481c7b056c4b410d28f33cf','path': 图片在本地的路径，如'full/7d97e98f8af710c7e7fe703abc8f639e0ee507c4.jpg','url': 原始地址，如'http://www.example.com/images/product1.jpg'})
    
    md5=Field()             #MD5值

    def __str__(self):
        return "NoteItem"
    
    def __init__(self,*kw):
        super(Note, self).__init__(*kw)
        self['collectionName']="Note"
        self['imageUrls']=[]
    
class MemberInfo(BaseItem):
    '''
    会员主页信息
    '''
    collectionName=Field()
    
    pageUrl = Field()
    name=Field() 
    currentAddress=Field() #现居
    email=Field()
    selfIntroduction=Field() #自我介绍
    joinDate=Field()
    comsumptionLevel=Field() #通常的旅行花费
    travalPurpose=Field() #大部分时候旅行是为了
    ageRange=Field() #年龄段
    gender=Field() #性别
    travelPreference=Field() #度假偏好
    travelPartner=Field() #通常和谁旅行
    
    trackGone=Field()   #去过哪
    trackKnow=Field()   #知道哪
    trackLike=Field()   #喜欢哪
    trackPlan=Field()   #计划去哪
    friends=Field()     #好友列表    

    def __str__(self):
        return "MemberInfo"
    
    def __init__(self,*kw):
        super(MemberInfo, self).__init__(*kw)
        self['collectionName']="MemberInfo"

class MemberTrack(BaseItem):
    '''
    会员足迹
    '''
    collectionName=Field()
    
    name=Field()
    gone=Field()
    know=Field()
    like=Field()
    plan=Field()

    def __str__(self):
        return "MemberTrack"
    
    def __init__(self,*kw):
        super(MemberTrack, self).__init__(*kw)
        self['collectionName']="MemberTrack"

class MemberFriend(BaseItem):
    '''
    会员好友
    '''
    collectionName=Field()
    
    #friends=Field() # like {friendName:address,friendName:address}
    name=Field()
    nameList = Field()
    cityList = Field()
    linkList = Field()
#    goneNumList = Field()
#    discoverList = Field()

    def __str__(self):
        return "MemberFriend"
    
    def __init__(self,*kw):
        super(MemberFriend, self).__init__(*kw)
        self['collectionName']="MemberFriend"

class MemberNoteList(BaseItem):
    '''
    会员游记
    '''
    collectionName="MemberNoteList"
    
    author = Field()
    titleList = Field()
    dateList = Field()
    
    pvNumList = Field()     #浏览量
    replyNumList = Field()  #回复    
    destinationList=Field() #旅游目的地
    imageUrls = Field()     #图片原始链接列表
    imagesInfo = Field()    #图片信息，是一个2元组列表。eg：(True 图片是否有效, {'checksum':图片MD5值，用于排重，如 '2b00042f7481c7b056c4b410d28f33cf','path': 图片在本地的路径，如'full/7d97e98f8af710c7e7fe703abc8f639e0ee507c4.jpg','url': 原始地址，如'http://www.example.com/images/product1.jpg'})

    def __str__(self):
        return "MemberNoteList"
    
    def __init__(self,*kw):
        super(MemberNoteList, self).__init__(*kw)
        self['collectionName']="MemberNoteList"
    
class Region(BaseItem):
    '''
    地区。包括了该地区的介绍、该地区的酒店
    '''
    collectionName=Field()
    name=Field()
    area=Field()
    introduction=Field()
    hotHotelLink=Field()
    
    def __str__(self):
        return "Region"
    
    def __init__(self,*kw):
        super(Region, self).__init__(*kw)
        self['collectionName']="Region"

class KeyWord(Item):
    '''
    搜索引擎关键字
    '''
    collectionName="KeyWord"
    keyWord=Field()
    itemCollectionName=Field() #关键字搜索出的item类别。必须是现有item之一，否则无法存储。 与ResponseBody的type相同
    priority=Field() #关键字优先级
    pageNumber=Field() #搜索页数
    
    optDateTime=Field() #最后一次搜索时间
    
    def __init__(self,*kw):
        super(KeyWord, self).__init__(*kw)
        self['collectionName']="KeyWord"
    
#class Image(Item):
#    '''
#    爬取结果中的图片
#    '''
#    collectionName="ImageDb"
#    imageUrl = Field() #图片原来的url
#    imagePath = Field() #图片存到本地的路径地址
    
