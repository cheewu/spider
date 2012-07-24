# -*- coding: utf-8 -*-
sohuSpider={
        'allowedDomains':[
        "travel.sohu.com", 
        "jingqu.travel.sohu.com", 
        "outdoor.travel.sohu.com"
    ],
        'startUrls':[                            
            'http://jingqu.travel.sohu.com',
            'http://travel.sohu.com',
        'http://outdoor.sohu.com/',

        ### 下面都是动态页面
        'http://outdoor.travel.sohu.com/s2006/1932/s241882226/', #业界动态
        'http://outdoor.travel.sohu.com/s2006/1932/s241882455/',  #徒步
        'http://outdoor.travel.sohu.com/s2006/1932/s241883133/', #空中运动
        'http://outdoor.travel.sohu.com/s2006/1932/s241883184/', #水域运动
        'http://outdoor.travel.sohu.com/dsty/', #都市体育
        'http://outdoor.travel.sohu.com/7/0404/55/column219995501.shtml', #环保公益
        'http://outdoor.travel.sohu.com/s2005/4860/s226184860.shtml', #校园户外
        'http://outdoor.travel.sohu.com/7/0404/96/column219959669.shtml', #活动公告

        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/', #登山·徒步
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_1.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_2.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_3.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_4.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_5.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_6.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_7.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_8.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_9.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_10.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_11.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_12.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_13.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_14.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_15.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_16.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_17.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_18.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_19.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_20.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_21.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882436/index_22.shtml',

        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/', #自驾·骑行
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_1.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_2.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_3.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_4.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_5.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_6.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_7.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_8.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_9.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_10.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_11.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_12.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_13.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_14.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_15.shtml',
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_16.shtml',        
        'http://outdoor.travel.sohu.com/s2006/1932/s241882679/index_17.shtml',

        'http://outdoor.travel.sohu.com/s2006/1932/s241882370/', #装备·体验
        'http://outdoor.travel.sohu.com/s2006/1932/s241882370/index_1.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882370/index_2.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882370/index_3.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882370/index_4.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882370/index_5.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882370/index_6.shtml', 

        'http://outdoor.travel.sohu.com/s2006/1932/s241882761/', #滑雪·攀岩
        'http://outdoor.travel.sohu.com/s2006/1932/s241882761/index_1.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882761/index_2.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882761/index_3.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882761/index_4.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882761/index_5.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882761/index_6.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882761/index_7.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882761/index_8.shtml', 
        'http://outdoor.travel.sohu.com/s2006/1932/s241882761/index_9.shtml', 

        'http://outdoor.travel.sohu.com/7/0404/48/column219954835.shtml', #全球户外山峰库
        
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
        #如：http://travel.sohu.com/s2009/7172/s264338530/
                'regex':'^http://travel\.sohu\.com/.*$',
                'priority':1000,
                'region':'//body',
            },
            {
        #如：http://jingqu.travel.sohu.com/j-102203.shtml
                'regex':'^http://jingqu\.travel\.sohu\.com/.*$',
                'priority':1000,
                'region':'//body',
            },
            {
        #如：http://outdoor.travel.sohu.com/s2006/1932/s241882761/index_9.shtml
                'regex':'^http://outdoor\.travel\.sohu\.com/.*$',
                'priority':1000,
                'region':'//body',
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            {
        #文章，如：
            #http://travel.sohu.com/20110921/n319974108.shtml
            #http://travel.sohu.com/20110921/n319974108_1.shtml
                'itemCollectionName':'Article1',
                'regex':'^http://travel\.sohu\.com/2\d{7}/n\d+(_\d+)?\.shtml$',
                'priority':600,
                'region':'//body',
            },    
            {
        #户外，如：#http://outdoor.sohu.com/20110929/n320960379.shtml
                'itemCollectionName':'Article2',
                'regex':'^http://outdoor\.sohu\.com/2\d{7}/n\d+(_\d+)?\.shtml$',
                'priority':600,'region':'//body',
            }
        ]
    
            }