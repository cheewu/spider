# -*- coding: utf-8 -*-
lvyou114Spider={
        'allowedDomains':["www.lvyou114.com" ],
        'startUrls':[                            
            'http://www.lvyou114.com/Youji/index.asp',
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
        #国内游记列表，如：
            #http://www.lvyou114.com/Youji/Class.asp?ClassID=1
            #http://www.lvyou114.com/Youji/class.asp?ClassID=1&page=2
                'regex':'^[Cc]{1}lass\.asp\?[Cc]{1}lassID=\d+(&page=\d+)?$',
                'priority':1000
            },
        {
        #国外游记列表，如：http://www.lvyou114.com/nav/Asia.asp
                'regex':'^\.\./nav/\w+\.asp$',
                'priority':1000
            },
        {
        #国外游记列表，如：http://www.lvyou114.com/nav/Nav_Class.asp?ClassID=73
                'regex':'^Nav_[Cc]{1}lass\.asp\?[Cc]{1}lassID=\d+(&page=\d+)?$',
                'priority':1000
            },
        {
        #国外游记列表，如： http://www.lvyou114.com/youji/Class.asp?ClassID=73
                'regex':'^http://www\.lvyou114\.com/youji/[Cc]{1}lass\.asp\?[Cc]{1}lassID=\d+(&page=\d+)?$',
                'priority':1000
            },
       
        
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
        #文章，如：http://www.lvyou114.com/Youji/25/25744.html
                'itemCollectionName':'Article',
                'regex':'^\d+/\d+\.html$',
                'priority':600
            },
        {
        #文章，如：http://www.lvyou114.com/Youji/25/25744.html
                'itemCollectionName':'Article',
                'regex':'^http://www\.lvyou114\.com/Youji/\d+/\d+\.html$',
                'priority':600
            }, 
        ]
    }