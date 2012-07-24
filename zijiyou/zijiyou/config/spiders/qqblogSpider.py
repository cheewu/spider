# -*- coding: utf-8 -*-
qqblogSpider={
        'allowedDomains':[
            "bbs.blog.qq.com",
        ],
        'startUrls':[
            'http://bbs.blog.qq.com/b-1001026847/l-1.htm',
        ],
        #普通list页正则表达式
        'normalRegex':[
        {
            #旅游博客列表，其中1001026847表示旅游内容BBS，如：http://bbs.blog.qq.com/b-1001026847/l-316.html
            'regex':'^/b\-1001026847/l\-\d+\.html$',
            'priority':1000
        }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            {
        #旅游博客文章，如：http://bbs.blog.qq.com/b-1001026847/17795.htm
                'itemCollectionName':'Article',
                'regex':'/b\-1001026847/\d+\.htm',
                'priority':500
            }  
        ]
    }