# -*- coding: utf-8 -*-
sinabbsSpider={
        'homePage':'http://club.travel.sina.com.cn',
        'allowedDomains':[
            "club.travel.sina.com.cn"
        ],
        'startUrls':[
            'http://club.travel.sina.com.cn/forum-2-1.html', #旅行天下
            'http://club.travel.sina.com.cn/forum-4-1.html', #驴友同行
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                #帖子列表分页，如：http://club.travel.sina.com.cn/forum-2-8.html
                'regex':r'^forum-\d+-\d+\.html$', 
                'priority':700, 
                
            }
        ], 
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            {
                #帖子文章，如：http://club.travel.sina.com.cn/thread-356808-1-1.html
                'itemCollectionName':'Article',
                'regex':r'^thread\-\d+\-\d+\-\d+\.html$',
                'region':'//div[@class="mainbox threadlist"]',
                'priority':1000
            },
        ]
                
    }