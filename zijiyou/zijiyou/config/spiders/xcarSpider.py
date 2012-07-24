# -*- coding: utf-8 -*-
xcarSpider={
        'allowedDomains':["xcar.com.cn"],
                'startUrls':[
            'http://www.xcar.com.cn/bbs/f175o14p1.html', #休闲生活
            'http://www.xcar.com.cn/bbs/f175o18p1.html', #自驾游记
            'http://www.xcar.com.cn/bbs/f175o68p1.html', #旅游手札
            'http://www.xcar.com.cn/bbs/f175o12p1.html', #吃喝FB
            'http://www.xcar.com.cn/bbs/f175o39p1.html', #小宠生活
            'http://www.xcar.com.cn/bbs/f175o64p1.html', #爱车生活
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                #【休闲生活】帖子列表分页，如：http://www.xcar.com.cn/bbs/f175o14p11.html
                'regex':r'f175o14p\d+\.html', 
                'priority':700, 
                'region':'//div[@class="FpageNum"]'
            },
            {
                #【自驾游记】帖子列表分页，如：http://www.xcar.com.cn/bbs/f175o18p36.html
                'regex':r'f175o18p\d+\.html', 
                'priority':700, 
                'region':'//div[@class="FpageNum"]'
            },
            {
                #【旅游手札】帖子列表分页，如：http://www.xcar.com.cn/bbs/f175o68p1.html
                'regex':r'f175o68p\d+\.html', 
                'priority':700, 
                'region':'//div[@class="FpageNum"]'
            },
            {
                #【吃喝FB】帖子列表分页，如：http://www.xcar.com.cn/bbs/f175o12p3.html
                'regex':r'f175o12p\d+\.html', 
                'priority':700, 
                'region':'//div[@class="FpageNum"]'
            },
            {
                #【小宠生活】帖子列表分页，如：http://www.xcar.com.cn/bbs/f175o39p1.html
                'regex':r'f175o39p\d+\.html', 
                'priority':700, 
                'region':'//div[@class="FpageNum"]'
            },
            {
                #【爱车生活】帖子列表分页，如：http://www.xcar.com.cn/bbs/f175o64p1.html
                'regex':r'f175o64p\d+\.html', 
                'priority':700, 
                'region':'//div[@class="FpageNum"]'
            },
                        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            {
                #帖子文章，如：http://www.xcar.com.cn/bbs/viewthread.php?tid=15446989
                'itemCollectionName':'BBSArticle',
                'regex':r'^viewthread\.php\?tid=\d+$',
                'priority':1000
            },
        ]                    
    }