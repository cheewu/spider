# -*- coding: utf-8 -*-
peopleSpider={
        'allowedDomains':["travel.people.com.cn" ],
        'startUrls':[ 
        #专题
        'http://travel.people.com.cn/GB/139035/index.html',

        #国内
        'http://travel.people.com.cn/GB/225668/index.html',

        #原创稿库
        'http://travel.people.com.cn/GB/203376/index.html',
        'http://travel.people.com.cn/GB/203376/index1.html',
        'http://travel.people.com.cn/GB/203376/index2.html',
        'http://travel.people.com.cn/GB/203376/index3.html',
        'http://travel.people.com.cn/GB/203376/index4.html',

        #旅游要闻
        'http://travel.people.com.cn/GB/41636/index.html',
        'http://travel.people.com.cn/GB/41636/index1.html',
        'http://travel.people.com.cn/GB/41636/index2.html',
        'http://travel.people.com.cn/GB/41636/index3.html',
        'http://travel.people.com.cn/GB/41636/index4.html',

        #旅游要闻>争鸣
        'http://travel.people.com.cn/GB/41636/41640/index.html',
        'http://travel.people.com.cn/GB/41636/41640/index1.html',
        'http://travel.people.com.cn/GB/41636/41640/index2.html',
        'http://travel.people.com.cn/GB/41636/41640/index3.html',
        
        #旅游要闻>国际
        'http://travel.people.com.cn/GB/41636/41641/index.html',
        'http://travel.people.com.cn/GB/41636/41641/index1.html',
        'http://travel.people.com.cn/GB/41636/41641/index2.html',
        'http://travel.people.com.cn/GB/41636/41641/index3.html',
        'http://travel.people.com.cn/GB/41636/41641/index4.html',

        #旅游要闻>业界
        'http://travel.people.com.cn/GB/41636/41644/index.html',
        'http://travel.people.com.cn/GB/41636/41644/index1.html',
        'http://travel.people.com.cn/GB/41636/41644/index2.html',
        'http://travel.people.com.cn/GB/41636/41644/index3.html',
        'http://travel.people.com.cn/GB/41636/41644/index4.html',

        
        ],
        #普通list页正则表达式
        'normalRegex':[
        {
        #国内列表，如：
            #http://travel.people.com.cn/GB/41636/41642/217441/index.html
            #http://travel.people.com.cn/GB/41636/41642/217441/index2.html
                'regex':'^http://travel\.people\.com\.cn/GB/41636/41642/\d+/index(\d+)?\.html$', 
                'priority':1000
            }        
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
        #文章，如：
            #http://travel.people.com.cn/GB/15569301.html
            #http://travel.people.com.cn/GB/198206/15755803.html
                'itemCollectionName':'Article',
                'regex':'^/GB/(\d+/)?\d+\.html$',
                'priority':600
            }  
        ]
    }