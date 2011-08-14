# -*- coding: utf-8 -*-

spiderConfig = {
                "baseSeSpider":{
                     'allowedDomains':[],
                     'startUrls':['http://blog.soso.com'],
                     'seUrlFormat':[{
                                     #搜索引擎名称
                                     'seName':'sosoBlog',
                                     #搜素格式
                                     'format':'http://blog.soso.com/qz.q?sc=qz&pid=qz.s.res&ty=blog&st=r&op=blog.blog&sd=0&w=%s&pg=%s',#搜索格式
#                                     'sePageNum':5,
                                     #输入编码
                                     'encode':'GBK',
                                     #搜素结果中，目标页的url的xpath
                                     'resultItemLinkXpath':'//div[2]/div[2]/div[2]/ol/li/a/@href',
                                     #搜素结果中，下一页搜素结果的xpath
                                     'nextPageLinkXpath':'//div[@class="page"]/div[@class="pg"]/a/@href',
                                     #搜素结果中搜素结果页数xpath
                                     'totalRecordXpath':'//div[@id="sNum"]/text()',
                                     #搜素结果中搜素结果页数
                                     'totalRecordRegex':r'[\d|,]+',
                                     #搜素引擎下一页的格式
                                     'nextPagePattern':'http://blog.soso.com/qz.q?w=keyWord&sc=qz&ty=blog&sd=0&st=r&cid=&op=blog.blog&pid=qz.s.res&pg=pageNum', #无法通过xpath获得js动态生成的下一页区域，使用模板
                                     #搜素引擎域
                                     'homePage':'http://blog.soso.com'                                  
                                     }],
                    'seXpath':{
                               #解析搜素结果页中的数据，如标题、发布时间、摘要、作者等
                               "sosoBlog":{
                                           #标题
                                           r'title':r'//ol/li/h3/a',
                                           #发布时间
                                           r'publishDate':r'//ol/li/h3/text()',
                                           #内容
                                           r'content':None,
                                           #摘要
                                           r'abstract':r'//ol/li'
                                           }
                               },
                     #普通list页正则表达式
                     'normalRegex':[
                                    "http://blog.soso.com/qz\.q"
                                    ],
                     #item页正则表达式 itemCollectionName对应item存放的数据表名
                     'itemRegex':[]
                     },
    "daodaoSpider":{
        'allowedDomains':["daodao.com"],
        'startUrls':[
                     'http://www.daodao.com/Lvyou'
                    ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':r'Tourism-g\d+-.*-Vacations\.html$', 
                'priority':10
            },
            {
                'regex':r'Attractions-g\d+-Activities-.*\.html$', 
                'priority':50
            },
            #包括游记列表、标签
            {
                'regex':r'Tourism-g\d+-c\d+-[^n].*\.html((\?pg=\d+)?|(\?kw=.*&st=8))$', 
                'priority':50
            } 
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #AttractionItem
            {
                'itemCollectionName':'Attraction',
                'regex':r'Attraction_Review-g\d+-.*-Reviews-.*\.html$', 
                'priority':600
            },  
            #NoteItem
            {
                'itemCollectionName':'Article',
                'regex':r'Tourism-g\d+-c\d+-n\d+.*\.html$', 
                'priority':500
            },              
            #CommonSenseItem
            {
                'itemCollectionName':'Note',
                'regex':r'Changshi-g\d+-.*\.html$', 
                'priority':500
            }
        ]
    },
    "yahooSpider":{
        'allowedDomains':["travel.cn.yahoo.com" ],
        'startUrls':[ 
            'http://travel.cn.yahoo.com/yxk/category/581/',
            'http://travel.cn.yahoo.com/yxk/category/586/',
            'http://travel.cn.yahoo.com/yxk/category/586/',
            'http://travel.cn.yahoo.com/yxk/category/574/',
            'http://travel.cn.yahoo.com/yxk/category/562/',
            'http://travel.cn.yahoo.com/yxk/category/557/',
            'http://travel.cn.yahoo.com/',
            'http://travel.cn.yahoo.com/travel_gonglve.html',			  
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':r'^http://travel.cn.yahoo.com/store/d+/$',
                'priority':1000
            },
            {
                'regex':r'^http://travel.cn.yahoo.com/area/\w+\.html$', 
                'priority':1000
            },
            {
                'regex':r'^http://travel.cn.yahoo.com/yxk/category/\d+/index_\d+.html$', 
                'priority':1000
            },
            {
                'regex':r'^http://travel.cn.yahoo.com/store/\d+/article-\d+-list.html$', 
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
                'itemCollectionName':'Article1',
                'regex':r'^http://travel.cn.yahoo.com/ypen/\d+/\d+\.html$',
                'priority':600
            },  
            {
                'itemCollectionName':'Article2',
                'regex':r'^http://travel.cn.yahoo.com/store/\d+/article-\d+-item.html$',
                'priority':600
            },
            {
                'itemCollectionName':'Article3',
                'regex':r'^http://travel.cn.yahoo.com/yxk/\d+/\w+.html$',
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
    },	
    "lvrenSpider":{
        'allowedDomains':["d.lvren.cn"],
        'startUrls':[ 
            'http://d.lvren.cn/guide/',
            'http://news.lvren.cn'
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':r'^http://news.lvren.cn/plus/list.php\?tid=\d+$', 
                'priority':1000
            },
            {
                'regex':r'^http://news.lvren.cn/plus/list.php\?tid=\d+&TotalResult=\d+&PageNo=\d+$', 
                'priority':1000
            },
            {
                'regex':r'^http://d.lvren.cn/youji/\w+/$', 'priority':1000
            },
            {
                'regex':r'^http://d.lvren.cn/youji/\w+_p\d+/$', 
                'priority':1000
            }
       ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
#            {
#                'itemCollectionName':'Article1',
#                'regex':r'^http://news.lvren.cn/html/.*\.html$',
#                'priority':600
#            },
            #Article
            {
                'itemCollectionName':'Article2',
                'regex':r'http://d.lvren.cn/gonglue/\w+/',
                'priority':600
            },  
            {
                'itemCollectionName':'Article3',
                'regex':r'http://d.lvren.cn/youji/\w+_\d+/',
                'priority':600
            }
        ]
    },
    "sozhenSpider":{
        'allowedDomains':["sozhen.com"],
        'startUrls':[
            'http://www.sozhen.com/'
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':r'^http://www.sozhen.com/\w+/$',
                'priority':1000
            },
            {
                'regex':r'^http://www.sozhen.com/default/chinatown_\d+.html$',
                'priority':1000
            },
            {
                'regex':r'^http://www.sozhen.com/default/townarticle_\d+.html$',
                'priority':1000
            },
            {
                'regex':r'^http://www.sozhen.com/default/newsarticle_\d+_\d+.html$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
            'itemCollectionName':'Article',
            'regex':r'^http://www.sozhen.com/default/\w+con_\d+_\d+.html$',
            'priority':600
            },  
        ]
    },


    "21cnSpider":{
        'allowedDomains':["travel.21cn.com"],
        'startUrls':[
            'http://travel.21cn.com/'
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':'http://travel.21cn.com/.*/list\d+.shtml',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
                'itemCollectionName':'Article',
                'regex':'http://travel\.21cn\.com/\w+/\w+/\d+/\d+/\d+/\d+\.shtml',
                'priority':600
            },
            #Article  
            {
                'itemCollectionName':'Article',
                'regex':'http://travel\.21cn\.com/\w+/\w+/\d+/\d+/\d+/\d+_\d+.shtml',
                'priority':600
            }  
        ]
    },
    "meishiSpider":{
        'allowedDomains':["meishiditu.com" ],
        'startUrls':[ 		                   
            'http://www.meishiditu.com/'
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':'^http://www.meishiditu.com/food/foodlist.php\?area=\w+&page=\d+$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
                'itemCollectionName':'Article',
                'regex':'^http://www.meishiditu.com/food/showpage.php\?id=\d+$',
                'priority':600
            }  
        ]
    },	
    "hexunSpider":{
        'allowedDomains':["travel.hexun.com" ],
        'startUrls':[ 		                   
            'http://travel.hexun.com'
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':'^http://travel.hexun.com/[^//]+/index(-\d+)*.html$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
                'itemCollectionName':'Article',
                'regex':'^http://travel.hexun.com/\d{4}-\d{2}-\d{2}/\d+(_\d+)*.html$',
                'priority':600
            }  
        ]
    },	
    "peopleSpider":{
        'allowedDomains':["travel.people.com.cn" ],
        'startUrls':[ 		                   
            'http://travel.people.com.cn'
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':'^http://travel.people.com.cn/GB/(\d+/)+index\d*.html$', 
                'priority':1000
            }
            ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
                'itemCollectionName':'Article',
                'regex':'^http://travel.people.com.cn/GB/(\d+/)*\d+.html$',
                'priority':600
            }  
        ]
    },	

    "sinaSpider":{
        'allowedDomains':["travel.sina.com.cn" ],
        'startUrls':[ 		                   
            'http://travel.sina.com.cn'
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':'^http://travel.sina.com.cn/.*/index.html$',
                'priority':1000
            },
            {
                'regex':'^http://travel.sina.com.cn/.*/$',
                'priority':1000
            },
            {
                'regex':'^http://travel.sina.com.cn/.*/list.html$',
                'priority':1000
            },
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
                'itemCollectionName':'Article1',
                'regex':'^http://travel.sina.com.cn/.*/\d+-\d+-\d+/\d+(_\d+)*.shtml$',
                'priority':600
            },  
            #Article
#            {
#                'itemCollectionName':'Article2',
#                'regex':'^http://blog.sina.com.cn/s/blog_\w+.html',
#                'priority':600
#            }  
        ]
    },	

    "lvyou114Spider":{
        'allowedDomains':["www.lvyou114.com" ],
        'startUrls':[ 		                   
            'http://www.lvyou114.com/Youji/'
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':'^http://www.lvyou114.com/Youji/[Cc]lass.asp\?[Cc]lassID=\d+(&page=\d+)*$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
                'itemCollectionName':'Article',
                'regex':'^http://www.lvyou114.com/Youji/\d+/\d+.html$',
                'priority':600
            },  
        ]
    },	

    "bbkerSpider":{
        'allowedDomains':["www.bbker.com" ],
        'startUrls':[ 		                   
            'http://www.bbker.com'
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':'^http://www.bbker.com/bbker/\w+(/doclist/)*(\w+.html)*$',
                'priority':1000
            },
#            {
#                'regex':'^http://www.bbker.com/tag/[%\w\d]+.html$',
#                'priority':1000
#            },
#            {
#                'regex':'^http://www.bbker.com/tag/doc/[%\w\d]+/(\d+.html)*$',
#                'priority':1000
#            },
            {
                'regex':'^http://www.bbker.com/bbker/\w+/doclist/volumn/[%\w\d]+/$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article 
            {
                'itemCollectionName':'Article',
                'regex':'^http://www.bbker.com/D\w+.html$',
                'priority':600
            }                                  
        ]
    },	
    "sohuSpider":{
        'allowedDomains':["travel.sohu.com" ,"jingqu.travel.sohu.com","outdoor.travel.sohu.com"],
        'startUrls':[ 		                   
            'http://jingqu.travel.sohu.com',
            'http://travel.sohu.com'	
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':'http://travel.sohu.com/\d+/n\d+.shtml',
                'priority':1000,
                'region':'//body',
            },
            {
                'regex':'^http://travel.sohu.com/.*$',
                'priority':1000,
                'region':'//body',
            },
            {
                'regex':'^http://jingqu.travel.sohu.com/.*$',
                'priority':1000,
                'region':'//body',
            },
            {
                'regex':'^http://outdoor.travel.sohu.com/.*$',
                'priority':1000,
                'region':'//body',
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            {
                'itemCollectionName':'Article1',
                'regex':'^http://travel.sohu.com/2\d{7}/n\d+(_\d+)*.shtml$',
                'priority':600,
                'region':'//body',
            },    
            {
                'itemCollectionName':'Article2',
                'regex':'^http://outdoor.travel.sohu.com/2\d{7}/n\d+(_\d+)*.shtml$',
                'priority':600,'region':'//body',
            },    
#            {
#                'itemCollectionName':'POI',
#                'regex':'^http://jingqu.travel.sohu.com/\w+-\d+.shtml$',
#                'priority':600,
#                'region':'//body',
#            },  
#            {
#                'itemCollectionName':'PICS',
#                'regex':'^http://pic.travel.sohu.com/group-\d+.shtml$',
#                'priority':600,
#                'region':'//body',
#            }, 
#            {
#                'itemCollectionName':'PICS',
#                'regex':'^ http://travel.sohu.com/\d+/\d+/travel_article\d+.shtml$',
#                'priority':600,
#                'region':'//body',
#            },  
        ]
    },	
    "lotourSpider":{
        'allowedDomains':[
            "d.lotour.com",
            "abroad.lotour.com" ,
            "outdoor.lotour.com",
            "leisure.lotour.com",
            "chn.lotour.com",
            "bjaround.lotour.com",
            "sharound.lotour.com",
            "gdaround.lotour.com",
            "scaround.lotour.com",
            "news.lotour.com",
            "golden.lotour.com"
        ],
        'startUrls':[                  
            "http://www.lotour.com/sitemap.html"
        ],
        #普通list页正则表达式
        'normalRegex':[		                   
            {
                'regex':'^http://\w+\.lotour\.com/\w+/index_\d+.shtml$',
                'priority':1000
            },
            {
                'regex':'^http://\w+\.lotour\.com/\w+/*$',
                'priority':1000
            },
            {
                'regex':'^http://\w+\.lotour\.com/*$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
#            {
#                'itemCollectionName':'POI',
#                'regex':'^http://d.lotour.com/\w+/*$',
#                'priority':1000
#            }, 
            {
                'itemCollectionName':'Article1',
                'regex':r'^http://\w+.lotour.com/\w+/20\d{6}/\w+\.shtml$',
                'priority':600
            },  
            {
                'itemCollectionName':'Article2',
                'regex':'^http://www.lotour.com/snapshot/\d+-\d+-\d+/snapshot(_\d+)+.shtml$',
                'priority':300
            }
        ]                     
    },

    "9tourSpider":{
        'allowedDomains':["www.9tour.cn"],
        'startUrls':[                  
            "http://www.9tour.cn/info/"
        ],
        #普通list页正则表达式
        'normalRegex':[		                   
            {
                'regex':'^http://www.9tour.cn/info/news_0_\d+_\d+/$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[              
            {
                'itemCollectionName':'Article',
                'regex':'^http://www.9tour.cn/info/\d+/\d+(_\d+)*.shtml$',
                'priority':300
            }
        ]                     
    },	

    "17uSpider":{
        'allowedDomains':["www.17u.com"],
        'startUrls':[ 		                   
            "http://www.17u.com",
        ],
        #普通list页正则表达式
        'normalRegex':[		                   
            {
                'regex':'^http://www.17u.com/news/newslist_\d+_\d+_\d+_c.html$',
                'priority':1000
            },
            {
                'regex':'^http://www.17u.com/blog/scenery/1951(_0/\d+)*$',
                'priority':1000
            },
            {
                'regex':'^http://www.17u.com/blog/\d+(/\d+)*$',
                'priority':1000
            },
            {
                'regex':'^http://www.17u.com/blog/cata/\d+$',
                'priority':1000
            },		
            {
                'regex':'^http://www.17u.com/blog/\w+/$',
                'priority':1000
            },
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
#            {
#                'itemCollectionName':'POI',
#                'regex':'^http://www.17u.com/destination/(scenery|city|province|country)_\d+.html$',
#                'priority':1000
#            }, 
            {
                'itemCollectionName':'Article1',
                'regex':'^http://www.17u.com/blog/article/\d+.html$',
                'priority':300
            },
            {
                'itemCollectionName':'Article2',
                'regex':'^http://www.17u.com/news/shownews\w+\.html$',
                'priority':600
            }, 
        ]         
    },	
		
    "mafengwoSpider":{
        'allowedDomains':["www.mafengwo.cn"],
        'startUrls':[ 		                   
            "http://www.mafengwo.cn"
        ],
        #普通list页正则表达式
        'normalRegex':[		                   
            {
                'regex':'^http://www.mafengwo.cn/mdd/smap.php\?mddid=\d+$',
                'priority':1000
            },
            {
                'regex':'^http://www.mafengwo.cn/mdd/detail.php\?mddid=\d+&sort=&start=\d+$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
#            {
#                'itemCollectionName':'POI',
#                'regex':'^http://www.mafengwo.cn/travel-scenic-spot/mafengwo/\d+.html$',
#                'priority':1000
#            }, 
#            {
#                'itemCollectionName':'Profile',
#                'regex':'^http://www.mafengwo.cn/u/\d+.html$',
#                'priority':1000
#            }, 
            {
                'itemCollectionName':'Article',
                'regex':'^http://www.mafengwo.cn/i/\d+.html$',
                'priority':600
            }, 
        ]
    },	

    "bytravelSpider":{
        'allowedDomains':["bytravel.cn"],
        'startUrls':[
            "http://www.bytravel.cn"
        ],
        #普通list页正则表达式
        'normalRegex':[		                   
            {
                'regex':'^http://\w+.bytravel.cn/{0,1}$',
                'priority':1000
            },
            {
                'regex':'^http://\w+.bytravel.cn/v/index\d+.html$',
                'priority':1000
            },
            {
                'regex':'^http://\w+.bytravel.cn/v/\d+/$',
                'priority':1000
            },
            {
                'regex':'^http://\w+.bytravel.cn/Scenery/[\w\d]+/(\d+/)*$',
                'priority':1000
            },
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            {
                'itemCollectionName':'Article1',
                'regex':'^http://\w+.bytravel.cn/art/[\d\w-]+/[\d\w\-\%\(\)\!]+/(index\d+.html)*$',
                'priority':1000
            }, 
            {
                'itemCollectionName':'Article1',
                'regex':'^http://\w+.bytravel.cn/(art|Scenery)/(.*).html$',
                'priority':1000
            },      
            {
                'itemCollectionName':'Article2',
                'regex':'^http://shop.bytravel.cn/produce/[\w\d]+/$',
                'priority':1000
            },  
        ]
    },	

    "QQBlogSpider":{
        'allowedDomains':[
            "blog.qq.com",
            "user.qzone.qq.com",
            "user.qzone.qq.com"
        ],
        'startUrls':[
            'http://blog.qq.com/travel/',
        ],
        #普通list页正则表达式
        'normalRegex':[

        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            {
                'itemCollectionName':'Article',
                'regex':'http://user.qzone.qq.com/\d+/blog/\d+',
                'priority':500
            },   
            {
                'itemCollectionName':'Article',
                'regex':'http://bbs.blog.qq.com/b-\d+/\d+\.htm',
                'priority':500
            },   
            {
                'itemCollectionName':'Article',
                'regex':'http://blog.qq.com/qzone/\d+/\d+\.htm',
                'priority':500
            },   
        ]
    },
		
           
    "lvpingSpider":{
        'allowedDomains':["lvping.com"],
        'startUrls':[
             #测试
            'http://www.lvping.com/Journals.aspx?type=2&title=&district=0&IsTitle=T&selecttype=2&orderby=r&pageindex=1',
            
#            'http://www.lvping.com/NorthAmericaNavigation.aspx',
#            'http://www.lvping.com/EuropeNavigation.aspx',
#            'http://www.lvping.com/AsiaNavigation.aspx',
#            'http://www.lvping.com/ChinaNavigation.aspx',
#            'http://www.lvping.com/OceaniaNavigation.aspx',
#            'http://www.lvping.com/southAmericaNavigation.aspx',
#            'http://www.lvping.com/AfricaNavigation.aspx',
#            
#            ##                                  #游记攻略
#            'http://www.lvping.com/Journals.aspx?type=1',
#            'http://www.lvping.com/Journals.aspx?selecttype=2',
#            'http://www.lvping.com/Journals.aspx',
        ],
        #普通list页正则表达式
        'normalRegex':[
            #测试
            {'regex':r'(/Journals\.aspx\?)?type=2&title=&district=0&IsTitle=T&selecttype=2&orderby=r&pageindex=.*', 'priority':200}, 
                       
#            {'regex':r'(http://www.lvping.com/)?(tourism)+-g\d+-\w+\.html$', 'priority':200}, #国家
#            {'regex':r'(http://www.lvping.com/)?(attractions-)+d\d+-\w+\.html$', 'priority':400}, #景点列表
#            {'regex':r'(http://www.lvping.com/)?(attractions-)+d\d+-s\d+-[r]+\w+\d+/\w+:\w+\.html$', 'priority':500}, #景点列表
#            {'regex':r'(http://www.lvping.com/)?(attractions-)+g\d+-\w+\.html$', 'priority':400}, #景点列表
#            {'regex':r'(http://www.lvping.com/)?(attractions-)+g\d+-[r]+\w+\d+-\w+\.html$', 'priority':450}, #景点列表
#            
#            {'regex':r'(http://www.lvping.com)?(/members/)+(\w/)+journals$', 'priority':700},# 会员游记列表
#            {'regex':r'(http://www.lvping.com)?/Journals.aspx\?.*selecttype=0.*', 'priority':700},# 游记列表
#            {'regex':r'(http://www.lvping.com)?/Journals.aspx\?.*selecttype=2.*', 'priority':700},# 攻略列表
#            {'regex':r'(http://www.lvping.com/)?(travel-)+d\d+-\w+\.html$', 'priority':400},    #常识列表页1
#            {'regex':r'(http://www.lvping.com/)?(travel-)+d\d+-\w+:brochure\.html#\w+', 'priority':400} #常识列表页2
        ],
        #item页正则表达式 type对应item存放的数据表名
        'itemRegex':[
            #测试
            {'itemCollectionName':'Article','regex':r'(http://www.lvping.com/)?(showjournal-)+d\d+-r\d+-journals+\.html$', 'priority':1000}, #攻略 作者 发表时间 浏览次数 评论次数
                     
#            {'itemCollectionName':'Note','regex':r'(http://www.lvping.com/)?(travel)+-d\d+-s\w?\d+/\w+:+\w+.*\.html$', 'priority':1000},  #国家介绍 概况、气候等常识
#            {'itemCollectionName':'Article','regex':r'(http://www.lvping.com/)?(travel-)+d1-+s\d+/\w+:\w+\.html$', 'priority':1000}, #短文攻略(类别 内容 目的地)
#            {'itemCollectionName':'Article','regex':r'(http://www.lvping.com/)?(showjournal-)+d\d+-r\d+-journals+\.html$', 'priority':1000}, #攻略 作者 发表时间 浏览次数 评论次数
#            {'itemCollectionName':'Article','regex':r'(http://www.lvping.com/)?journals/AllSingleJournals.aspx\?Writing=\d+$', 'priority':1000}, #第二种攻略游记情况 http://www.lvping.com/journals/AllSingleJournals.aspx?Writing=1322380
#            {'itemCollectionName':'MemberInfo','regex':r'(http://www.lvping.com/)?(members/)+\w+$', 'priority':1}, #用户
#            #                                  {'itemCollectionName':'MemberTrack','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/travelmap-public)+$', 'priority':1}, #足迹
#            {'itemCollectionName':'MemberFriend','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/friends)+$', 'priority':1}, #好友
#            {'itemCollectionName':'MemberNoteList','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/journals)+$', 'priority':1},  #游记MemberNoteList','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/journals)+$', 'priority':1},  #游记
#            
#            {'itemCollectionName':'Attraction','regex':r'(http://www.lvping.com/)?(attraction_review-)+d\d+-s\d+-[(detail)(attraction)]+\.html$', 'priority':1000}, #景点
#            {'itemCollectionName':'Region', 'regex':r'(http://www.lvping.com)?(/tourism-)+d\d+-\w+\.html$', 'priority':300}, #城市景区
        ],
        'imageXpath':['//div[@class="yjDetail cf"]//img/@src']
    },
            #------------------------------------------------------------------------------------------------------------------------------------
            "bbsSpider":{
                     'homePage':'http://www.go2eu.com/bbs/', #后面要加 /
                     'allowedDomains':["go2eu.com"],
                     'startUrls':['http://www.19lou.com/forum-1174-filter-type-typeid-566-1.html'],
                     #普通list页正则表达式
                     'normalRegex':[
                                    {'regex':r'forumdisplay.php\?fid=\d+.*page=\d+$|forum-\d+-\d+.html$', 'priority':700},
                                    ],
                     #item页正则表达式 itemCollectionName对应item存放的数据表名
                     'itemRegex':[
                                  {'itemCollectionName':'Article', 'regex':r'viewthread.php\?.*tid=\d+.*$|thread-\d+-\d+-\d+.html$'},
                                  ],
                     'firstPageItemRegex':'viewthread.php\?(tid=\d+)?((?!page=).)*$|thread-\d+-1-\d+.html$',
                     'maxPageNumXpath':'//span[@class="threadpages"]/a[last()]/@href',
                     'maxPageNumRegex':None,
                     'pagePattern':{'page=(\d+)':'page=%s', '-(\d)+-':'-%s-'},
                     'itemPriority':1100
                     },


	      "bbsSpider2":{
                     'allowedDomains':['www.go2eu.com'],
                     'startUrls':[
                                  'http://www.go2eu.com/bbs/viewthread.php?action=printable&tid=93313'
#                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=79&page=1'
                                  ],
                     #普通list页正则表达式
                     'normalRegex':[
#                                    {'regex':r'forumdisplay.php\?fid=\d+', 'priority':700, 'region':'//div/div[@class="pages"]'}, #列表后续页，在板块页中找 &page=\d+$
                                    ],
                     #item页正则表达式 itemCollectionName对应item存放的数据表名
                     'itemRegex':[
                                  {'itemCollectionName':'Article',
                                   'regex':r'(viewthread\.php\?tid=\d+&extra=page.{1,4}\d+)|(http://www\.go2eu\.com/bbs/viewthread\.php\?action=printable&tid=.*)',
                                   'itemPrintPageFormat':r'http://www.go2eu.com/bbs/viewthread.php?action=printable&tid=%s',
                                   'itemTidRegex':r'tid=(\d+)',
                                   'region':'//div/form/table',
                                   'priority':1000},
                                  ]
                     },

	      "55bbsSpider":{
                     'allowedDomains':["bbs.55bbs.com"],
                     'startUrls':[
                                  'http://bbs.55bbs.com/thread-5730685-1-1.html',
#                                  'http://bbs.55bbs.com/forum-34-1.html'
                                  ],
		      #普通list页正则表达式
		     'normalRegex':[
			     {'regex':r'forum-34-\d+.html$', 'priority':1000, 'region':'//div[@class="pages"]'},
				    ],
		     #item页正则表达式 itemCollectionName对应item存放的数据表名
		     'itemRegex':[
                                 {'itemCollectionName':'Article',
                                  'regex':r'(thread-\d+-1-\d+.html)|(http:\/\/bbs\.55bbs\.com\/viewthread\.php\?action=printable&tid=.*)',
                                  'itemPrintPageFormat':r'http://bbs.55bbs.com/viewthread.php?action=printable&tid=%s',
                                  'itemTidRegex':r'thread-(\d+)',
                                  'region':'//div[@class="mainbox threadlist"]',
                                  'priority':1000},
                                 ]
		    
                     },
           
	      'go2euSpider':{
                           'allowedDomains':["go2eu.com"],
                           'startUrls':[
                                #测试
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=98',
                                
                                        
#                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=12', #德国
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=14', #法国
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=13', #意大利
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=17', #荷比卢
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=18', #西班牙葡萄牙
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=19', #奥地利
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=16', #英国
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=15', #瑞士
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=26', #希腊土耳其
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=25', #北欧
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=24', #东欧
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=58', #东南亚
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=57', #东亚
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=59', #西亚南亚
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=51', #中国
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=52', #港澳台
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=53', #美国
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=54', #加拿大
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=55', #拉美
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=56', #澳大利亚
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=83', #新西兰
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=86', #埃及
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=60', #非洲
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=94', #游轮
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=3', #签证
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=1', #多国
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=62', #廉航
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=79', #交通
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=33', #自驾
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=80', #购物
#            					'http://www.go2eu.com/bbs/forumdisplay.php?fid=100', #银联
					           ],
			    
			     #普通list页正则表达式
			     'normalRegex':[
        					    {'regex':r'forumdisplay.php\?fid=\d+', 'priority':700, 'region':'//div/div[@class="pages"]'}, #列表后续页，在板块页中找 &page=\d+$
        					   ],
			     #item页正则表达式 itemCollectionName对应item存放的数据表名
			     'itemRegex':[
                                  {'itemCollectionName':'BBSArticle',
                                   'regex':r'(viewthread\.php\?tid=\d+&extra=page.{1,4}\d+)|(http://www\.go2eu\.com/bbs/viewthread\.php\?action=printable&tid=.*)',
                                   'itemPrintPageFormat':r'http://www.go2eu.com/bbs/viewthread.php?action=printable&tid=%s',
                                   'itemTidRegex':r'tid=(\d+)',
                                   'region':'//div/form/table',
                                   'priority':1000},
                                  ]
					
                },


	   "lvyeSpider":{
                       'allowedDomains':["bbs.lvye.cn"],
                       'startUrls':[
                                    'http://bbs.lvye.cn/forum-viewthread-action-printable-tid-318979.html'
                                #'http://bbs.lvye.cn/forum-1559-1.html',#自驾
				#'htp://bbs.lvye.cn/forum-8-1.html',#游记攻略
				#'http://bbs.lvye.cn/forum-1815-1.html',#背包自助
				#'http://bbs.lvye.cn/forum-354-1.html',#户外摄影
#				'http://bbs.lvye.cn/forum-haiwai-1.html'#海外
		        ],
		     
		      #普通list页正则表达式
		     'normalRegex':[
                                 {'regex':r'forum-\d+-\d+.html$', 'priority':700, 'region':'//div[@class="pg"]'}, #帖子列表页
                                  {'regex':r'forum-haiwai-\d+.html$', 'priority':700, 'region':'//div[@class="pg"]'}, #帖子列表页
                                   ],
		     #item页正则表达式 itemCollectionName对应item存放的数据表名
		     'itemRegex':[
                                 {'itemCollectionName':'Article',
                                  'regex':r'(thread-\d+-1-\d+.html)|(http:\/\/bbs\.lvye\.cn\/forum-viewthread-action-printable-tid-\d+\.html)',
                                  'itemPrintPageFormat':r'http://bbs.lvye.cn/forum-viewthread-action-printable-tid-%s.html',
                                  'itemTidRegex':r'thread-(\d+)',
                                  'region':'//div[@class="bm_c"]',
                                  'priority':1000},
                                 ]
		    
                     },
	 'sinabbsSpider':{
                           'homePage':'http://club.travel.sina.com.cn',
                           'allowedDomains':["club.travel.sina.com.cn"],
                           'startUrls':[
                                        'http://club.travel.sina.com.cn/thread-349694-1-1.html',
#                                        'http://club.travel.sina.com.cn/forum-2-1.html', #旅行天下
#					'http://club.travel.sina.com.cn/forum-4-1.html', #驴友同行
#					'http://club.travel.sina.com.cn/forum-21-1.html', #光影记录
                                        ],
                            #普通list页正则表达式
                            'normalRegex':[
#                                            {'regex':r'forum-\d+-\d+.html$', 'priority':700, 'region':'//div[@class="pages"]'}, #帖子列表页
                                           
                                            ],
                            #item页正则表达式 itemCollectionName对应item存放的数据表名
                            'itemRegex':[
                                 {'itemCollectionName':'Article',
                                  'regex':r'(thread-\d+-1-\d+.html)|(http:\/\/club\.travel\.sina\.com\.cn\/viewthread.php\?action=printable&tid=\d+)',
                                  'itemPrintPageFormat':r'http://club.travel.sina.com.cn/viewthread.php?action=printable&tid=%s',
                                  'itemTidRegex':r'thread-(\d+)',
                                  'region':'//div[@class="mainbox threadlist"]',
                                  'priority':1000},
                                 ]
			    
          },

	  'xcarSpider':{
                           'allowedDomains':["xcar.com.cn"],
                           'startUrls':[
                                        'http://www.xcar.com.cn/bbs/forumdisplay.php?fid=175'
					],
			    
			     #普通list页正则表达式
			     'normalRegex':[
					    {'regex':r'forumdisplay.php\?fid=175&page=\d+', 'priority':700, 'region':'//div[@class="FpageNum"]'}, #列表页，在板块页中找 
					    ],
			     #item页正则表达式 itemCollectionName对应item存放的数据表名
			     'itemRegex':[
                                  {'itemCollectionName':'BBSArticle',
                                   'regex':r'(viewthread\.php\?tid=\d+)|(http:\/\/www\.xcar\.com\.cn\/bbs\/viewthread\.php\?action=printable&tid=\d+)',
                                   'itemPrintPageFormat':r'http://www.xcar.com.cn/bbs/viewthread.php?action=printable&tid=%s',
                                   'itemTidRegex':r'tid=(\d+)',
                                   'region':'//div[@class="maintable"]',
                                   'priority':1000},
                                  ]
					
          },


	'lotourbbsSpider':{
                           'allowedDomains':["bbs.lotour.com"],
                           'startUrls':[
                                        'http://bbs.lotour.com/forum-2-1.html', #行游中国
					'http://bbs.lotour.com/forum-18-1.html', #异域风情
					'http://bbs.lotour.com/forum-10-1.html' , #光影天堂
					'http://bbs.lotour.com/forum-58-1.html', #美食生活
					'http://bbs.lotour.com/forum-210-1.html', #旅游热讯
					'http://bbs.lotour.com/forum-2-1.html' #行游中国
					],
			    
			    #普通list页正则表达式
                            'normalRegex':[
                                            {'regex':r'forum-\d+-\d+.html$', 'priority':700, 'region':'//div[@class="pages"]'}, #帖子列表页
                                           
                                            ],
                            #item页正则表达式 itemCollectionName对应item存放的数据表名
                            'itemRegex':[
                                 {'itemCollectionName':'Article',
                                  'regex':r'(thread-\d+-1-\d+.html)|(http:\/\/bbs.lotour.com\/viewthread.php\?action=printable&tid=\d+)',
                                  'itemPrintPageFormat':r'http://bbs.lotour.com/viewthread.php?action=printable&tid=%s',
                                  'itemTidRegex':r'thread-(\d+)',
                                  'region':'//div[@id="threadlist"]',
                                  'priority':1000},
                                 ]
					
          },





}














