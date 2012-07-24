# -*- coding: utf-8 -*-
yahooSpider={
        'allowedDomains':["travel.cn.yahoo.com" ],
        'startUrls':[ 
            'http://travel.cn.yahoo.com/yxk/category/581/', #国内计划
            'http://travel.cn.yahoo.com/yxk/category/586/', #环球风情
            'http://travel.cn.yahoo.com/yxk/category/574/', #吃喝玩乐
            'http://travel.cn.yahoo.com/yxk/category/562/', #自助游
            'http://travel.cn.yahoo.com/yxk/category/557/', #团队游
            'http://travel.cn.yahoo.com/event/gonglv/', #出行攻略
        'http://travel.cn.yahoo.com/event/miaozhao/', #旅游妙招
        ],
        #普通list页正则表达式
        'normalRegex':[
#        几乎都是图片，以后如果需要，再配置抓取
#            {
#                'regex':r'^http://travel.cn.yahoo.com/store/d+/$',
#                'priority':1000
#            },
#            {
#                'regex':r'^http://travel.cn.yahoo.com/area/\w+\.html$', 
#                'priority':1000
#            },
            {
        #列表：国内计划、环球风情、吃喝玩乐、自助游、团队游，如：
        #http://travel.cn.yahoo.com/yxk/category/581/index_2.html
                'regex':r'^/yxk/category/\d+/index_\d+\.html$', 
                'priority':1000
            },
            {
        #列表：景区资讯、美食推荐、景区交通、旅游指南，如：http://travel.cn.yahoo.com/store/48/article-2-list.html
                #'regex':r'^http://travel\.cn\.yahoo\.com/store/\d+/article-\d+-list\.html$', 
        'regex':r'^/store/\d+/article-\d+-list.html$', 
                'priority':1000
            },
        {
        #列表：出行攻略、旅行妙招，如：
        #http://travel.cn.yahoo.com/event/miaozhao/?page=2
        #http://travel.cn.yahoo.com/event/gonglv/?page=7
                'regex':r'^\?page=\d+$', 
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
        #文章：出行攻略、旅行妙招，如：http://travel.cn.yahoo.com/ypen/20110426/329462.html
                'itemCollectionName':'Article1',
                'regex':r'^http://travel\.cn\.yahoo\.com/ypen/\d+/\d+\.html$',
                'priority':600
            },  
            {
        #文章：旅游咨询，旅游攻略，如：http://travel.cn.yahoo.com/store/278/article-2477-item.html
                'itemCollectionName':'Article2',
                #'regex':r'^http://travel\.cn\.yahoo\.com/store/\d+/article-\d+-item\.html$',
                'regex':r'^/store/\d+/article-\d+-item.html$',
                'priority':600
            },
            {
        #文章：国内计划，环球风情，吃喝玩乐，自助游，团队游，如：
        #http://travel.cn.yahoo.com/yxk/20110617/6p-s.html
        #http://travel.cn.yahoo.com/yxk/20110622/6qgs.html
                'itemCollectionName':'Article3',
                #'regex':r'^http://travel\.cn\.yahoo\.com/yxk/\d+/\w+\.html$',
                'regex':r'^/yxk/\d+/[\w-]+.html$',
                'priority':600
            },
#            {
#                'itemCollectionName':'Article',
#                'regex':r'^http://travel.cn.yahoo.com/newspic/travel/\d+/$', 
#                'priority':600
#            },
#            {
#                'itemCollectionName':'Article4',
#                'regex':r'^http://travel.cn.yahoo.com/newspic/travel/\d+/\d+/$', 
#                'priority':600
#            }
        ]
    }