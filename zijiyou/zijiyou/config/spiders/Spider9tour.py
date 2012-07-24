# -*- coding: utf-8 -*-
Spider9tour={
        'allowedDomains':["www.9tour.cn"],
        'startUrls':[                  
            "http://www.9tour.cn/info/"
        ],
        #普通list页正则表达式
        'normalRegex':[                           
            {
        #列表，如：http://www.9tour.cn/info/news_0_0_6/
                'regex':'^/info/news_0_\d+_\d+/$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[              
            {
        #文章，如：
            #http://www.9tour.cn/info/248/296760.shtml
            #http://www.9tour.cn/info/248/296760_2.shtml
                'itemCollectionName':'Article',
                'regex':'^/info/\d+/\d+(_\d+)*\.shtml$',
                'priority':300
            }
        ]                     
    }