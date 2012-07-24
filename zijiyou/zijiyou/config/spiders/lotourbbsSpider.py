# -*- coding: utf-8 -*-
lotourbbsSpider={
        'allowedDomains':["bbs.lotour.com"],
                'startUrls':[
            'http://bbs.lotour.com/forumdisplay.php?fid=2&filter=type&typeid=1', #行游中国：游记攻略
            'http://bbs.lotour.com/forumdisplay.php?fid=2&filter=type&typeid=136', #行游中国：自驾游天下
            'http://bbs.lotour.com/forumdisplay.php?fid=18&filter=type&typeid=1', #异域风情：游记攻略
            'http://bbs.lotour.com/forumdisplay.php?fid=10&filter=type&typeid=142' , #光影天堂：风光美图
            'http://bbs.lotour.com/forumdisplay.php?fid=58&filter=type&typeid=144', #美食生活：地方美食
            'http://bbs.lotour.com/forumdisplay.php?fid=210&filter=type&typeid=145', #旅游热讯：打折活动
            'http://bbs.lotour.com/forumdisplay.php?fid=210&filter=type&typeid=148', #旅游热讯：租车导游
            'http://bbs.lotour.com/forumdisplay.php?fid=210&filter=type&typeid=146', #旅游热讯：旅行线路
            'http://bbs.lotour.com/forumdisplay.php?fid=210&filter=type&typeid=147', #旅游热讯：优惠住宿
            'http://bbs.lotour.com/forumdisplay.php?fid=210&filter=type&typeid=150', #旅游热讯：景点门票
        ],                
        #普通list页正则表达式
        'normalRegex':[
            {
                #【行游中国：游记攻略】列表，如：http://bbs.lotour.com/forumdisplay.php?fid=2&filter=type&typeid=1&page=9
                'regex':r'^forumdisplay\.php\?fid=2&filter=type&typeid=1&page=\d+$', 
                'priority':700, 
                'region':'//div[@class="pages"]'
            },
            {
                #【行游中国：自驾天下】列表，如：http://bbs.lotour.com/forumdisplay.php?fid=2&filter=type&typeid=136&page=5
                'regex':r'^forumdisplay\.php\?fid=2&filter=type&typeid=13&page=\d+$', 
                'priority':700, 
                'region':'//div[@class="pages"]'
            },

            {
                #【异域风情：游记攻略】列表，如：http://bbs.lotour.com/forumdisplay.php?fid=18&filter=type&typeid=1&page=10
                'regex':r'^forumdisplay\.php\?fid=18&filter=type&typeid=1&page=\d+$', 
                'priority':700, 
                'region':'//div[@class="pages"]'
            },
            
            {
                #【光影天堂：风光美图】列表，如：http://bbs.lotour.com/forumdisplay.php?fid=10&filter=type&typeid=142&page=8
                'regex':r'^forumdisplay\.php\?fid=10&filter=type&typeid=142&page=\d+$', 
                'priority':700, 
                'region':'//div[@class="pages"]'
            },
            
            {
                #【美食生活：地方美食】列表，如：http://bbs.lotour.com/forumdisplay.php?fid=58&filter=type&typeid=144&page=5
                'regex':r'^forumdisplay\.php\?fid=58&filter=type&typeid=144&page=\d+$', 
                'priority':700, 
                'region':'//div[@class="pages"]'
            },
            
            {
                #【旅游热讯：打折活动】列表，如：http://bbs.lotour.com/forumdisplay.php?fid=210&filter=type&typeid=145&page=10
                'regex':r'^forumdisplay\.php\?fid=210&filter=type&typeid=145&page=\d+$', 
                'priority':700, 
                'region':'//div[@class="pages"]'
            }, 
            {
                #【旅游热讯：租车导游】列表，如：http://bbs.lotour.com/forumdisplay.php?fid=210&filter=type&typeid=148&page=6
                'regex':r'^forumdisplay\.php\?fid=210&filter=type&typeid=148&page=\d+$', 
                'priority':700, 
                'region':'//div[@class="pages"]'
            },
            {
                #【旅游热讯：旅行线路】列表，如：http://bbs.lotour.com/forumdisplay.php?fid=210&filter=type&typeid=146&page=9
                'regex':r'^forumdisplay\.php\?fid=210&filter=type&typeid=146&page=\d+$', 
                'priority':700, 
                'region':'//div[@class="pages"]'
            }, 
            {
                #【旅游热讯：优惠住宿】列表，如：http://bbs.lotour.com/forumdisplay.php?fid=210&filter=type&typeid=147&page=8
                'regex':r'^forumdisplay\.php\?fid=210&filter=type&typeid=147&page=\d+$', 
                'priority':700, 
                'region':'//div[@class="pages"]'
            },
            {
                #【旅游热讯：景点门票】列表，如：http://bbs.lotour.com/forumdisplay.php?fid=210&filter=type&typeid=150&page=6
                'regex':r'^forumdisplay\.php\?fid=210&filter=type&typeid=150&page=\d+$', 
                'priority':700, 
                'region':'//div[@class="pages"]'
            }
        ],            
        #item页正则表达式 itemCollectionName对应item存放的数据表名
#！！！！！！！！！！！！！！不使用打印的页面，直接拿到论坛的主题帖（配置xpath的时候注意一下）
        'itemRegex':[
            {
                #论坛帖子主题文章页面，如：http://bbs.lotour.com/viewthread.php?tid=435425&extra=page%3D1%26amp%3Bfilter%3Dtype%26amp%3Btypeid%3D136
                'itemCollectionName':'Article',
                                'regex':r'^viewthread\.php\?tid=\d+.+typeid.+(1)?(136)?(142)?(144)?(145)?(146)?(147)?(148)?(150)?$',
                                'region':'//div[@id="threadlist"]',
                                'priority':1000
            },
            {
                #论坛帖子主题文章页面，如：
                'itemCollectionName':'Article',
                                'regex':r'^viewthread\.php\?tid=\d+.+typeid.+1$',
                                'region':'//div[@id="threadlist"]',
                                'priority':1000
            },
            {
                #论坛帖子主题文章页面，如：http://bbs.lotour.com/viewthread.php?tid=435425&extra=page%3D1%26amp%3Bfilter%3Dtype%26amp%3Btypeid%3D136
                'itemCollectionName':'Article',
                                'regex':r'^viewthread\.php\?tid=\d+.+typeid.+136$',
                                'region':'//div[@id="threadlist"]',
                                'priority':1000
            },
            {
                #论坛帖子主题文章页面，如：
                'itemCollectionName':'Article',
                                'regex':r'^viewthread\.php\?tid=\d+.+typeid.+142$',
                                'region':'//div[@id="threadlist"]',
                                'priority':1000
            },
            {
                #论坛帖子主题文章页面，如：
                'itemCollectionName':'Article',
                                'regex':r'^viewthread\.php\?tid=\d+.+typeid.+144$',
                                'region':'//div[@id="threadlist"]',
                                'priority':1000
            },
            {
                #论坛帖子主题文章页面，如：
                'itemCollectionName':'Article',
                                'regex':r'^viewthread\.php\?tid=\d+.+typeid.+145$',
                                'region':'//div[@id="threadlist"]',
                                'priority':1000
            },
            {
                #论坛帖子主题文章页面，如：
                'itemCollectionName':'Article',
                                'regex':r'^viewthread\.php\?tid=\d+.+typeid.+146$',
                                'region':'//div[@id="threadlist"]',
                                'priority':1000
            },
            {
                #论坛帖子主题文章页面，如：
                'itemCollectionName':'Article',
                                'regex':r'^viewthread\.php\?tid=\d+.+typeid.+147$',
                                'region':'//div[@id="threadlist"]',
                                'priority':1000
            },
            {
                #论坛帖子主题文章页面，如：
                'itemCollectionName':'Article',
                                'regex':r'^viewthread\.php\?tid=\d+.+typeid.+148$',
                                'region':'//div[@id="threadlist"]',
                                'priority':1000
            },
            {
                #论坛帖子主题文章页面，如：
                'itemCollectionName':'Article',
                                'regex':r'^viewthread\.php\?tid=\d+.+typeid.+150$',
                                'region':'//div[@id="threadlist"]',
                                'priority':1000
            },
        ]                    
    }