# -*- coding: utf-8 -*-
Spider17u={
        'allowedDomains':["www.17u.com"],
        'startUrls':[                            
            "http://www.17u.com",
        "http://www.17u.com/news/", 
        "http://www.17u.com/blog/",
        'http://www.17u.com/blog/best/', #精华博客
        'http://www.17u.com/blog/my/', #真我博客
        'http://www.17u.com/blog/cata/19889', #出行攻略
        ],
        #普通list页正则表达式
        'normalRegex':[                           
            {
        #资讯，如：http://www.17u.com/news/newslist_33_26_0_c.html
                'regex':'^/news/newslist_\d+_\d+_\d+_c\.html$',
                'priority':1000
            },
        {
        #精华博客列表分页，如：http://www.17u.com/blog/best/2
                'regex':'^/blog/best/\d+$',
                'priority':1000
            },
        {
        #真我博客列表分页，如：http://www.17u.com/blog/my/2
                'regex':'^/blog/my/\d+$',
                'priority':1000
            },
        {
        #列表分页，如：http://www.17u.com/blog/cata/19889/21
                'regex':'^/blog/cata/\d+(/\d+)?$',
                'priority':1000
            },
        {
        #如：
            #http://www.17u.com/blog/area/226
            #http://www.17u.com/blog/area/226/3
                'regex':'^/blog/area/\d+(/\d+)?$',
                'priority':1000
            },
        {
        #如：
            #http://www.17u.com/blog/scenery/1951
            #http://www.17u.com/blog/scenery/1951_0/3
                'regex':'^/blog/scenery/\d+(_\d/\d+)?$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
#            {
#                'itemCollectionName':'POI',
#                'regex':'^http://www.17u.com/destination/(scenery|city|province|country)_\d+.html$',
#                'priority':1000
#            }, 
         {
        #博客文章，如：http://www.17u.com/blog/article/789010.html
                'itemCollectionName':'Article1',
                'regex':'^/blog/article/\d+\.html$',
                'priority':300
            },
            {
        #如：http://www.17u.com/news/shownews_1531131_0_c.html
                'itemCollectionName':'Article2',
                'regex':'^/news/shownews\w+\.html$',
                'priority':600
            }, 
        ]         
    }