# -*- coding: utf-8 -*-
meishiSpider={
        'allowedDomains':["meishiditu.com" ],
        'startUrls':[                            
            'http://www.meishiditu.com/'
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
        #美食列表，如：http://www.meishiditu.com/food/foodlist.php?area=beijing&page=1
                'regex':'^/food/foodlist\.php\?area=\w+&page=\d+$',
                'priority':1000
            },
        {
        #美食列表：分页，如：http://www.meishiditu.com/food/foodlist.php?area=beijing&classified=&page=9
                'regex':'^\?area=\w+&classified=&page=\d+$',
                'priority':1000
            }        
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
        #美食文章，如：http://www.meishiditu.com/food/showpage.php?id=21098
                'itemCollectionName':'Article',
                'regex':'^http://www\.meishiditu\.com/food/showpage\.php\?id=\d+$',
                'priority':600
            }  
        ]
    }