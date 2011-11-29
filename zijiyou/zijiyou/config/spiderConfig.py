# -*- coding: utf-8 -*-

spiderConfig = {
                "baseSeSpider":{
                     'allowedDomains':[],
                     'startUrls':['http://blog.soso.com'],
                     'seUrlFormat':[
#                                    {
#                                     #搜索引擎名称
#                                     'seName':'sosoBlog',
#                                     #搜素格式
#                                     'format':'http://blog.soso.com/qz.q?sc=qz&pid=qz.s.res&ty=blog&st=r&op=blog.blog&sd=0&w=%s&pg=%s',#搜索格式
#                                     #输入编码
#                                     'encode':'GBK',
#                                     #搜素结果中，目标页的url的xpath
#                                     'resultItemLinkXpath':'//div[2]/div[2]/div[2]/ol/li',
#                                     #搜素结果中搜素结果页数xpath
#                                     'totalRecordXpath':'//div[@id="sNum"]/text()',
#                                     #搜素结果中搜素结果页数
#                                     'totalRecordRegex':r'[\d|,]+',
#                                     #搜素引擎下一页的格式
#                                     'nextPagePattern':'http://blog.soso.com/qz.q?w=keyWord&sc=qz&ty=blog&sd=0&st=r&cid=&op=blog.blog&pid=qz.s.res&pg=pageNum',
#                                     #搜素引擎域
#                                     'homePage':'http://blog.soso.com'                                  
#                                     },
                                    {
                                     #搜索引擎名称
                                     'seName':'qihoo',
                                     #搜素格式
                                     'format':'http://www.qihoo.com/wenda.php?kw=%s&do=search&src=wenda_search&area=0&page=%s',#搜索格式
                                     #输入编码
                                     'encode':'GBK',
                                     #搜素结果中，目标页的url的xpath
                                     'resultItemLinkXpath':'//body/table//tr/td[2]/div/table//tr/td',
                                     #搜素结果中搜素结果页数xpath
                                     'totalRecordXpath':'//table//tr/td[2]/table//tr/td/div/em/text()',
                                     #搜素结果中搜素结果页数
                                     'totalRecordRegex':r'[\d|,]+',
                                     #搜素引擎下一页的格式
                                     'nextPagePattern':'http://www.qihoo.com/wenda.php?kw=%s&do=search&src=wenda_search&area=0&page=%s',
                                     #搜素引擎域
                                     'homePage':'http://www.qihoo.com'
                                     }
                                    ],
                    'seXpath':{
                               #解析搜素结果页中的数据，如标题、发布时间、摘要、作者等
                               "sosoBlog":{
                                           #标题
                                           r'title':r'h3/a//text()',
                                           #发布时间
                                           r'publishDate':r'h3/text()',
                                           #内容
                                           r'content':'//body',
                                           #摘要
                                           r'abstract':r'text()',
                                           #原文链接
                                           r'originUrl':r'h3/a/@href',
                                           #url链接
                                           r'url':r'a/@href'
                                           },
                                "qihoo":{
                                           #标题
                                           r'title':r'a/font//text()',
                                           #发布时间
                                           r'publishDate':r'font[1]/text()',
                                           #内容
                                           r'content':'//body',
                                           #摘要
                                           r'abstract':r'font[3]/text()',
                                           #原文链接
                                           r'originUrl':r'a/@href',
                                           #url链接
                                           r'urlRegex':r'<!-- <a href="(\S*)" target="_blank" class=m>正文快照</a>'
                                           }
                               },
                     #普通list页正则表达式
                     'normalRegex':[
                                    "http://blog.soso.com/qz\.q",
                                    "http://www.qihoo.com.*"
                                    ],
                     #item页正则表达式 itemCollectionName对应item存放的数据表名
                     'itemRegex':[]
                     },

    "daodaoSpider":{
        'allowedDomains':["daodao.com"],
        'startUrls':[
#                        #国内旅游
#                        'http://www.daodao.com/Tourism-g297450-c0-Liaoning.html',
#                        'http://www.daodao.com/Tourism-g297441-c0-Jiangsu.html',
#                        'http://www.daodao.com/Tourism-g297468-c0-Zhejiang.html',
#                        'http://www.daodao.com/Tourism-g297455-c0-Shandong.html',
#                        'http://www.daodao.com/Tourism-g297411-c0-Guangdong.html',
#                        'http://www.daodao.com/Tourism-g297436-c0-Hubei.html',
#                        'http://www.daodao.com/Tourism-g297462-c0-Sichuan.html',
#                        'http://www.daodao.com/Tourism-g297460-c0-Shanxi.html',
#                        'http://www.daodao.com/Tourism-g303738-c0-Hunan.html',
#                        'http://www.daodao.com/Tourism-g297467-c0-Yunnan.html',
#                        #直辖市
#                        'http://www.daodao.com/Tourism-g294212-c0-Beijing.html',
#                        'http://www.daodao.com/Tourism-g308272-c0-Shanghai.html',
#                        'http://www.daodao.com/Tourism-g294213-c0-Chongqing.html',
#                        'http://www.daodao.com/Tourism-g311293-c0-Tianjin.html',
#                        #港澳台
#                        'http://www.daodao.com/Tourism-g294217-c0-Hong_Kong_Hong_Kong_Region.html',
#                        'http://www.daodao.com/Tourism-g664891-c0-Macau_Macau_Region.html',
#                        'http://www.daodao.com/Tourism-g293910-c0-Taiwan.html',
#                        #65个国外热门国家旅游
#                        'http://www.daodao.com/Tourism-g294265-c0-Singapore.html',
#                        'http://www.daodao.com/Tourism-g294265-c0-Singapore.html',
#                        'http://www.daodao.com/Tourism-g293915-c0-Thailand.html',
#                        'http://www.daodao.com/Tourism-g294196-c0-South_Korea.html',
#                        'http://www.daodao.com/Tourism-g293921-c0-Vietnam.html',
#                        'http://www.daodao.com/Tourism-g294443-c0-North_Korea.html',
#                        'http://www.daodao.com/Tourism-g293951-c0-Malaysia.html',
#                        'http://www.daodao.com/Tourism-g255055-c0-Australia.html',
#                        'http://www.daodao.com/Tourism-g293889-c0-Nepal.html',
#                        'http://www.daodao.com/Tourism-g191-c0-United_States.html',
#                        'http://www.daodao.com/Tourism-g294200-c0-Egypt.html',
#                        'http://www.daodao.com/Tourism-g293939-c0-Cambodia.html',
#                        'http://www.daodao.com/Tourism-g294245-c0-Philippines.html',
#                        'http://www.daodao.com/Tourism-g293740-c0-South_Africa.html',
#                        'http://www.daodao.com/Tourism-g293969-c0-Turkey.html',
#                        'http://www.daodao.com/Tourism-g186216-c0-United_Kingdom.html',
#                        'http://www.daodao.com/Tourism-g187070-c0-France.html',
#                        'http://www.daodao.com/Tourism-g294459-c0-Russia.html',
#                        'http://www.daodao.com/Tourism-g188045-c0-Switzerland.html',
#                        'http://www.daodao.com/Tourism-g294206-c0-Kenya.html',
#                        'http://www.daodao.com/Tourism-g293860-c0-India.html',
#                        'http://www.daodao.com/Tourism-g187427-c0-Spain.html',
#                        'http://www.daodao.com/Tourism-g153339-c0-Canada.html',
#                        'http://www.daodao.com/Tourism-g189398-c0-Greece.html',
#                        'http://www.daodao.com/Tourism-g255104-c0-New_Zealand.html',
#                        'http://www.daodao.com/Tourism-g187275-c0-Germany.html',
#                        'http://www.daodao.com/Tourism-g187768-c0-Italy.html',
#                        'http://www.daodao.com/Tourism-g294190-c0-Myanmar.html',
#                        'http://www.daodao.com/Tourism-g294331-c0-Fiji.html',
#                        'http://www.daodao.com/Tourism-g293949-c0-Laos.html',
#                        'http://www.daodao.com/Tourism-g190410-c0-Austria.html',
#                        'http://www.daodao.com/Tourism-g293977-c0-Israel.html',
#                        'http://www.daodao.com/Tourism-g293844-c0-Bhutan.html',
#                        'http://www.daodao.com/Tourism-g189952-c0-Iceland.html',
#                        'http://www.daodao.com/Tourism-g189806-c0-Sweden.html',
#                        'http://www.daodao.com/Tourism-g294473-c0-Ukraine.html',
#                        'http://www.daodao.com/Tourism-g188553-c0-The_Netherlands.html',
#                        'http://www.daodao.com/Tourism-g293961-c0-Sri_Lanka.html',
#                        'http://www.daodao.com/Tourism-g293738-c0-Seychelles.html',
#                        'http://www.daodao.com/Tourism-g293955-c0-Mongolia.html',
#                        'http://www.daodao.com/Tourism-g294280-c0-Brazil.html',
#                        'http://www.daodao.com/Tourism-g293730-c0-Morocco.html',
#                        'http://www.daodao.com/Tourism-g190455-c0-Norway.html',
#                        'http://www.daodao.com/Tourism-g294012-c0-United_Arab_Emirates.html',
#                        'http://www.daodao.com/Tourism-g190311-c0-Malta.html',
#                        'http://www.daodao.com/Tourism-g274684-c0-Czech_Republic.html',
#                        'http://www.daodao.com/Tourism-g294266-c0-Argentina.html',
#                        'http://www.daodao.com/Tourism-g189896-c0-Finland.html',
#                        'http://www.daodao.com/Tourism-g274881-c0-Hungary.html',
#                        'http://www.daodao.com/Tourism-g190405-c0-Monaco.html',
#                        'http://www.daodao.com/Tourism-g190340-c0-Luxembourg.html',
#                        'http://www.daodao.com/Tourism-g189100-c0-Portugal.html',
#                        'http://www.daodao.com/Tourism-g294225-c0-Indonesia.html',
#                        'http://www.daodao.com/Tourism-g294137-c0-Samoa.html',
#                        'http://www.daodao.com/Tourism-g188634-c0-Belgium.html',
#                        'http://www.daodao.com/Tourism-g293753-c0-Tunisia.html',
#                        'http://www.daodao.com/Tourism-g293747-c0-Tanzania.html',
#                        'http://www.daodao.com/Tourism-g293959-c0-Pakistan.html',
#                        'http://www.daodao.com/Tourism-g190372-c0-Cyprus.html',
#                        'http://www.daodao.com/Tourism-g293985-c0-Jordan.html',
#                        'http://www.daodao.com/Tourism-g293998-c0-Iran.html',
#                        'http://www.daodao.com/Tourism-g274960-c0-Latvia.html',
#                        'http://www.daodao.com/Tourism-g189512-c0-Denmark.html',
#                        'http://www.daodao.com/Tourism-g150768-c0-Mexico.html',
#                        'http://www.daodao.com/Tourism-g186591-c0-Ireland.html',
                        'http://www.daodao.com/Tourism-g293953-c0-Maldives.html',
                    ],
        #普通list页正则表达式
        'normalRegex':[
                       #下一页
                       {
                        'regex':r'Tourism-g\d+-c0-[\w_]+\.html\?pg=\d+$',
                        'priority':100,
                        'region':'//div[@id="result"]/div[1]/div[1]',
                        'multitype':False#是否既为list页，也为item页。如果只为list，则不执行item页保存判断
                        }
                       ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
                     #AttractionItem
                     {
                      'itemCollectionName':'Article',
                      'regex':r'Tourism-g\d+[-\w\d_]+[\w\d_]+\.html$',
                      'priority':1000,
                      'region':'//div[@id="result"]/div[2]',
                      'multitype':False#是否既为list页，也为item页。如果只为list，则不执行item页保存判断
                      },
                     ]
    },

    "yahooSpider":{
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
    },    

    "lvrenSpider":{
        'allowedDomains':["d.lvren.cn"],
        'startUrls':[ 
        'http://d.lvren.cn/guide/',
        'http://d.lvren.cn/china/',
        'http://d.lvren.cn/world/',
        'http://news.lvren.cn/html/lvyouzixun/',
        'http://news.lvren.cn/html/gedilvyou/',
        'http://news.lvren.cn/html/huwaipindao/',
        'http://news.lvren.cn/html/jiudianpindao/',
        'http://news.lvren.cn/html/xianluyouji/'
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
        #列表：分页
        'regex':r'^list_\d+_\d+.html$',
                'priority':1000
            },
        {
        #如：http://d.lvren.cn/guide/scenic_48173/
                'regex':r'^/guide/\w+/$', 
        'priority':1000
            },

        {
        #获取包含游记的页面，如：http://d.lvren.cn/lvyou/yunnandali/
                'regex':r'^/lvyou/\w+/$', 
        'priority':1000
            },
        {
        #获取游记列表，如：http://d.lvren.cn/youji/yunnandali/
                'regex':r'^/youji/\w+/$', 
        'priority':1000
            },
            {
        #获取游记列表：分页页面，如：http://d.lvren.cn/youji/yunnandali_p2/
                'regex':r'^/youji/\w+_p\d+/$', 
                'priority':1000
            }        
       ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article 文章
        {
        #旅游资讯，如：http://news.lvren.cn/html/lvyouzixun/201109/2748492.html
                'itemCollectionName':'Article1',
         'regex':r'^/html/lvyouzixun/\d+/\d+(_\d+)?\.html$',
                'priority':600
            },
        {
        #旅游资讯，如：
            #各地美食：http://news.lvren.cn/html/lvyouzixun/gedimeishi/201108/3048286.html
            #旅游天气：http://news.lvren.cn/html/lvyouzixun/weather/201012/2146395.html
            #出境旅游：http://news.lvren.cn/html/lvyouzixun/chujinglvyou/201109/2148450.html
            #旅游新闻：http://news.lvren.cn/html/lvyouzixun/news/201109/2848500.html
                'itemCollectionName':'Article1',
         'regex':r'^/html/lvyouzixun/[a-zA-Z]+/\d+/\d+(_\d+)?\.html$',
                'priority':600
            },
            {
        #各地旅游，如：http://news.lvren.cn/html/gedilvyou/beijinglvyou/201106/2847832.html
                'itemCollectionName':'Article1',
         'regex':r'^/html/gedilvyou/[a-zA-Z]+/\d+/\d+(_\d+)?\.html$',
                'priority':600
            },
        {
        #各地旅游，如：http://news.lvren.cn/html/lvyou//201011/3046220.html
                'itemCollectionName':'Article1',
         'regex':r'^/html/lvyou//\d+/\d+(_\d+)?\.html$',
                'priority':600
            },
         {
        #户外频道，如：http://news.lvren.cn/html/huwaixinwen/2010/0322/41560.html
                'itemCollectionName':'Article1',
         'regex':r'^/html/huwaixinwen/\d+/\d+/\d+(_\d+)?\.html$',
                'priority':600
            },
        {
        #户外频道，如：http://news.lvren.cn/html/huwaipindao/hangyebaodao/2010/0316/41525.html
                'itemCollectionName':'Article1',
         'regex':r'^/html/huwaipindao/[a-zA-Z]+/\d+/\d+/\d+(_\d+)?\.html$',
                'priority':600
            },
        {
        #酒店频道，如：http://news.lvren.cn/html/jiudianpindao/201001/1537815.html
                'itemCollectionName':'Article1',
         'regex':r'^/html/jiudianpindao/\d+/\d+(_\d+)?\.html$',
                'priority':600
            },
        {
        #线路游记，如：http://news.lvren.cn/html/xianluyouji/2010/0222/41105.html
                'itemCollectionName':'Article1',
         'regex':r'^/html/xianluyouji/\d+/\d+/\d+(_\d+)?\.html$',
                'priority':600
            },
        {
        #线路游记，如：http://news.lvren.cn/html/xianluyouji/beijinglvyougonglue/2010/0223/41188.html
                'itemCollectionName':'Article1',
         'regex':r'^/html/xianluyouji/[a-zA-Z]+/\d+/\d+/\d+(_\d+)?\.html$',
                'priority':600
            },
        {
        #游人攻略，如：http://d.lvren.cn/gonglue/dongjing/
                'itemCollectionName':'Article2',
                'regex':r'^/gonglue/\w+/$',
                'priority':600
            }, 
        {
        #游记文章，如：http://d.lvren.cn/youji/yunnandali_100930/
                'itemCollectionName':'Article3',
                'regex':r'/youji/\w+_\d+/',
                'priority':600
            }
        ]
    },

    "sozhenSpider":{
        'allowedDomains':["sozhen.com"],
        'startUrls':[
            'http://www.sozhen.com/default/chinaprovince.html', #中国古镇
        'http://www.sozhen.com/default/newsarticle.html' #古镇新闻
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
        #某个古镇列表，如：http://www.sozhen.com/default/chinatown_12.html
                'regex':r'^chinatown_\d+\.html$',
                'priority':1000
            },
        {
        #古镇新闻列表：分页，如：http://www.sozhen.com/default/newsarticle_0_10.html
                'regex':r'^newsarticle_0_\d+\.html$',
                'priority':1000
            },
        {
        #某个客栈游记攻略列表（含分页），如：
            #http://www.sozhen.com/default/towninn_12.html
            #http://www.sozhen.com/default/towninn_12_7.html
                'regex':r'^/default/towninn_\d+(_\d+)?\.html$',
                'priority':1000
            },
        {
        #某个古镇游记攻略列表（含分页），如：
            #http://www.sozhen.com/default/townarticle_62.html
            #http://www.sozhen.com/default/townarticle_62_1.html
                'regex':r'^\.\./default/townarticle_\d+(_\d+)?\.html$',
                'priority':1000
            },            
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
        #文章内容，如：http://www.sozhen.com/default/townarticlecon_12_52358.html
        'itemCollectionName':'Article',
        'regex':r'^/default/\w+con_\d+_\d+\.html$',
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
        #列表，如：http://travel.21cn.com/scene/foreign/list1.shtml
                'regex':'^http://travel\.21cn\.com/.*/list\d+\.shtml$',
                'priority':1000
            },
        {
        #列表（含分页），如：http://travel.21cn.com/scene/foreign/list2.shtml
                'regex':'^list\d+\.shtml$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
        #文章页面，如：http://travel.21cn.com/outdoor/tubu/2007/08/17/3422364.shtml
                'itemCollectionName':'Article',
                'regex':'http://travel\.21cn\.com/\w+/\w+/\d+/\d+/\d+/\d+\.shtml',
                'priority':600
            },
            #Article  
            {
        #含分页的文章，如：http://travel.21cn.com/guide/senery/2011/09/27/9268652_2.shtml
                'itemCollectionName':'Article',
                'regex':'^\d+_\d+\.shtml$',
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
    },

    "hexunSpider":{
        'allowedDomains':["travel.hexun.com" ],
        'startUrls':[                            
            'http://travel.hexun.com',
        
        #国内景点列表
        'http://travel.hexun.com/chinese-travel/index.html',
        'http://travel.hexun.com/chinese-travel/index-1.html',
        'http://travel.hexun.com/chinese-travel/index-2.html',
        'http://travel.hexun.com/chinese-travel/index-3.html',
        'http://travel.hexun.com/chinese-travel/index-4.html',
        'http://travel.hexun.com/chinese-travel/index-5.html',
        'http://travel.hexun.com/chinese-travel/index-6.html',
        'http://travel.hexun.com/chinese-travel/index-7.html',
        'http://travel.hexun.com/chinese-travel/index-8.html',
        'http://travel.hexun.com/chinese-travel/index-9.html',
        'http://travel.hexun.com/chinese-travel/index-10.html',
        'http://travel.hexun.com/chinese-travel/index-11.html',
        'http://travel.hexun.com/chinese-travel/index-12.html',
        'http://travel.hexun.com/chinese-travel/index-13.html',
        'http://travel.hexun.com/chinese-travel/index-14.html',
        'http://travel.hexun.com/chinese-travel/index-15.html',
        'http://travel.hexun.com/chinese-travel/index-16.html',
        'http://travel.hexun.com/chinese-travel/index-17.html',
        'http://travel.hexun.com/chinese-travel/index-18.html',
        'http://travel.hexun.com/chinese-travel/index-19.html',
        'http://travel.hexun.com/chinese-travel/index-20.html',
        'http://travel.hexun.com/chinese-travel/index-21.html',
        'http://travel.hexun.com/chinese-travel/index-22.html',
        'http://travel.hexun.com/chinese-travel/index-23.html',
        'http://travel.hexun.com/chinese-travel/index-24.html',
        'http://travel.hexun.com/chinese-travel/index-25.html',
        'http://travel.hexun.com/chinese-travel/index-26.html',
        'http://travel.hexun.com/chinese-travel/index-27.html',
        'http://travel.hexun.com/chinese-travel/index-28.html',
        'http://travel.hexun.com/chinese-travel/index-29.html',
        'http://travel.hexun.com/chinese-travel/index-30.html',
        'http://travel.hexun.com/chinese-travel/index-31.html',
        'http://travel.hexun.com/chinese-travel/index-32.html',
        'http://travel.hexun.com/chinese-travel/index-33.html',
        'http://travel.hexun.com/chinese-travel/index-34.html',
        'http://travel.hexun.com/chinese-travel/index-35.html',
        'http://travel.hexun.com/chinese-travel/index-36.html',
        'http://travel.hexun.com/chinese-travel/index-37.html',
        'http://travel.hexun.com/chinese-travel/index-38.html',
        'http://travel.hexun.com/chinese-travel/index-39.html',
        'http://travel.hexun.com/chinese-travel/index-40.html',

        #国外景点列表
        'http://travel.hexun.com/overseas-travel/index.html',
        'http://travel.hexun.com/overseas-travel/index-1.html',
        'http://travel.hexun.com/overseas-travel/index-2.html',
        'http://travel.hexun.com/overseas-travel/index-3.html',
        'http://travel.hexun.com/overseas-travel/index-4.html',
        'http://travel.hexun.com/overseas-travel/index-5.html',
        'http://travel.hexun.com/overseas-travel/index-6.html',
        'http://travel.hexun.com/overseas-travel/index-7.html',
        'http://travel.hexun.com/overseas-travel/index-8.html',
        'http://travel.hexun.com/overseas-travel/index-9.html',
        'http://travel.hexun.com/overseas-travel/index-10.html',
        'http://travel.hexun.com/overseas-travel/index-11.html',
        'http://travel.hexun.com/overseas-travel/index-12.html',
        'http://travel.hexun.com/overseas-travel/index-13.html',
        'http://travel.hexun.com/overseas-travel/index-14.html',
        'http://travel.hexun.com/overseas-travel/index-15.html',
        'http://travel.hexun.com/overseas-travel/index-16.html',
        'http://travel.hexun.com/overseas-travel/index-17.html',
        'http://travel.hexun.com/overseas-travel/index-18.html',
        'http://travel.hexun.com/overseas-travel/index-19.html',
        'http://travel.hexun.com/overseas-travel/index-20.html',
        'http://travel.hexun.com/overseas-travel/index-21.html',
        'http://travel.hexun.com/overseas-travel/index-22.html',
        'http://travel.hexun.com/overseas-travel/index-23.html',
        'http://travel.hexun.com/overseas-travel/index-24.html',
        'http://travel.hexun.com/overseas-travel/index-25.html',
        'http://travel.hexun.com/overseas-travel/index-26.html',
        
        #美食列表
        'http://travel.hexun.com/food/index.html',
        'http://travel.hexun.com/food/index-1.html',
        'http://travel.hexun.com/food/index-2.html',
        'http://travel.hexun.com/preparations/index.html',
        'http://travel.hexun.com/preparations/index-1.html',
        'http://travel.hexun.com/preparations/index-2.html',
        'http://travel.hexun.com/preparations/index-3.html',
        'http://travel.hexun.com/preparations/index-4.html',
        'http://travel.hexun.com/preparations/index-5.html',
        'http://travel.hexun.com/preparations/index-6.html',
        
        #产业资讯
        'http://travel.hexun.com/news/',

        #解读新政
        'http://travel.hexun.com/policies/index.html',
        'http://travel.hexun.com/policies/index-1.html',
        'http://travel.hexun.com/policies/index-2.html',
        'http://travel.hexun.com/policies/index-3.html',

        #新兴旅游
        'http://travel.hexun.com/new-way/index.html',
        'http://travel.hexun.com/new-way/index-1.html',
        'http://travel.hexun.com/new-way/index-2.html',
        'http://travel.hexun.com/new-way/index-3.html',
        'http://travel.hexun.com/new-way/index-4.html',
        'http://travel.hexun.com/new-way/index-5.html',
        'http://travel.hexun.com/new-way/index-6.html',

        #旅游评论
        'http://travel.hexun.com/commentary/index.html',
        'http://travel.hexun.com/commentary/index-1.html',
        'http://travel.hexun.com/commentary/index-2.html',
        'http://travel.hexun.com/commentary/index-3.html',
        'http://travel.hexun.com/commentary/index-4.html',
        'http://travel.hexun.com/commentary/index-5.html',
        'http://travel.hexun.com/commentary/index-6.html',
        'http://travel.hexun.com/commentary/index-7.html',
        'http://travel.hexun.com/commentary/index-8.html',
        'http://travel.hexun.com/commentary/index-9.html',

        #户外运动
        'http://travel.hexun.com/outdoors/index.html',
        'http://travel.hexun.com/outdoors/index-1.html',
        'http://travel.hexun.com/outdoors/index-2.html',
        'http://travel.hexun.com/outdoors/index-3.html',
        'http://travel.hexun.com/outdoors/index-4.html',
        'http://travel.hexun.com/outdoors/index-5.html',
        'http://travel.hexun.com/outdoors/index-6.html',
        'http://travel.hexun.com/outdoors/index-7.html',
        'http://travel.hexun.com/outdoors/index-8.html',
        'http://travel.hexun.com/outdoors/index-9.html',
        'http://travel.hexun.com/outdoors/index-10.html',
        'http://travel.hexun.com/outdoors/index-11.html',
        'http://travel.hexun.com/outdoors/index-12.html',
        'http://travel.hexun.com/outdoors/index-13.html',
        'http://travel.hexun.com/outdoors/index-14.html',
        'http://travel.hexun.com/outdoors/index-15.html',
        'http://travel.hexun.com/outdoors/index-16.html',
        'http://travel.hexun.com/outdoors/index-17.html',

        #旅游超市
        'http://travel.hexun.com/supermarket/index.html',

        #出行信息
        'http://travel.hexun.com/trip-information/index.html',
        'http://travel.hexun.com/trip-information/index-1.html',
        'http://travel.hexun.com/trip-information/index-2.html',
        'http://travel.hexun.com/trip-information/index-3.html',
        'http://travel.hexun.com/trip-information/index-4.html',
        'http://travel.hexun.com/trip-information/index-5.html',
        'http://travel.hexun.com/trip-information/index-6.html',
        'http://travel.hexun.com/trip-information/index-7.html',
        'http://travel.hexun.com/trip-information/index-8.html',
        'http://travel.hexun.com/trip-information/index-9.html',
        'http://travel.hexun.com/trip-information/index-10.html',
        'http://travel.hexun.com/trip-information/index-11.html',
        'http://travel.hexun.com/trip-information/index-12.html',
        'http://travel.hexun.com/trip-information/index-13.html',
        'http://travel.hexun.com/trip-information/index-14.html',
        'http://travel.hexun.com/trip-information/index-15.html',
        'http://travel.hexun.com/trip-information/index-16.html',
        'http://travel.hexun.com/trip-information/index-17.html',
        'http://travel.hexun.com/trip-information/index-18.html',
        'http://travel.hexun.com/trip-information/index-19.html',
        'http://travel.hexun.com/trip-information/index-20.html',
        'http://travel.hexun.com/trip-information/index-21.html',
        'http://travel.hexun.com/trip-information/index-22.html',
        'http://travel.hexun.com/trip-information/index-23.html',
        'http://travel.hexun.com/trip-information/index-24.html',
        'http://travel.hexun.com/trip-information/index-25.html',
        'http://travel.hexun.com/trip-information/index-26.html',
        'http://travel.hexun.com/trip-information/index-27.html',
        'http://travel.hexun.com/trip-information/index-28.html',
        'http://travel.hexun.com/trip-information/index-29.html',
        'http://travel.hexun.com/trip-information/index-30.html',
        'http://travel.hexun.com/trip-information/index-31.html',
        'http://travel.hexun.com/trip-information/index-32.html',
        'http://travel.hexun.com/trip-information/index-33.html',
        'http://travel.hexun.com/trip-information/index-34.html',
        'http://travel.hexun.com/trip-information/index-35.html',
        'http://travel.hexun.com/trip-information/index-36.html',
        'http://travel.hexun.com/trip-information/index-37.html',
        'http://travel.hexun.com/trip-information/index-38.html',
        'http://travel.hexun.com/trip-information/index-39.html',
        'http://travel.hexun.com/trip-information/index-40.html',
        'http://travel.hexun.com/trip-information/index-41.html',
        'http://travel.hexun.com/trip-information/index-42.html',
        'http://travel.hexun.com/trip-information/index-43.html',

        #酒店会所
        'http://travel.hexun.com/hotel-club/index.html',
        'http://travel.hexun.com/hotel-club/index-1.html',
        'http://travel.hexun.com/hotel-club/index-2.html',
        'http://travel.hexun.com/hotel-club/index-3.html',
        'http://travel.hexun.com/hotel-club/index-4.html',
        'http://travel.hexun.com/hotel-club/index-5.html',
        'http://travel.hexun.com/hotel-club/index-6.html',
        'http://travel.hexun.com/hotel-club/index-7.html',
        'http://travel.hexun.com/hotel-club/index-8.html',
        'http://travel.hexun.com/hotel-club/index-9.html',
        'http://travel.hexun.com/hotel-club/index-10.html',
        'http://travel.hexun.com/hotel-club/index-11.html',
        'http://travel.hexun.com/hotel-club/index-12.html',

        #精品会展
        'http://travel.hexun.com/exhibitions/index.html',
        'http://travel.hexun.com/exhibitions/index-1.html',
        'http://travel.hexun.com/exhibitions/index-2.html',
        'http://travel.hexun.com/exhibitions/index-3.html',
        'http://travel.hexun.com/exhibitions/index-4.html',
        'http://travel.hexun.com/exhibitions/index-5.html',
        'http://travel.hexun.com/exhibitions/index-6.html',
        'http://travel.hexun.com/exhibitions/index-7.html',
        'http://travel.hexun.com/exhibitions/index-8.html',
        'http://travel.hexun.com/exhibitions/index-9.html',
        'http://travel.hexun.com/exhibitions/index-10.html',
        'http://travel.hexun.com/exhibitions/index-11.html',
        'http://travel.hexun.com/exhibitions/index-12.html',
        'http://travel.hexun.com/exhibitions/index-13.html',
        'http://travel.hexun.com/exhibitions/index-14.html',
        'http://travel.hexun.com/exhibitions/index-15.html',
        'http://travel.hexun.com/exhibitions/index-16.html',
        'http://travel.hexun.com/exhibitions/index-17.html',
        'http://travel.hexun.com/exhibitions/index-18.html',
        'http://travel.hexun.com/exhibitions/index-19.html',
        'http://travel.hexun.com/exhibitions/index-20.html',
        'http://travel.hexun.com/exhibitions/index-21.html',
        'http://travel.hexun.com/exhibitions/index-22.html',
        'http://travel.hexun.com/exhibitions/index-23.html',
        'http://travel.hexun.com/exhibitions/index-24.html',
        'http://travel.hexun.com/exhibitions/index-25.html',
        'http://travel.hexun.com/exhibitions/index-26.html',
        'http://travel.hexun.com/exhibitions/index-27.html',
        'http://travel.hexun.com/exhibitions/index-28.html',

        #旅行家
        'http://travel.hexun.com/traveler/index.html',
        'http://travel.hexun.com/traveler/index-1.html',
        'http://travel.hexun.com/traveler/index-2.html',
        'http://travel.hexun.com/traveler/index-3.html',
        'http://travel.hexun.com/traveler/index-4.html',

        #星游闻
        'http://travel.hexun.com/star-travel/index.html',
        'http://travel.hexun.com/star-travel/index-1.html',
        'http://travel.hexun.com/star-travel/index-2.html',
        'http://travel.hexun.com/star-travel/index-3.html',
        'http://travel.hexun.com/star-travel/index-4.html',
        'http://travel.hexun.com/star-travel/index-5.html',
        'http://travel.hexun.com/star-travel/index-6.html',
        'http://travel.hexun.com/star-travel/index-7.html',
        'http://travel.hexun.com/star-travel/index-8.html',
        'http://travel.hexun.com/star-travel/index-9.html',

        #旅途视频秀
        'http://travel.hexun.com/tvshow/index.html',
        'http://travel.hexun.com/tvshow/index-1.html',
        'http://travel.hexun.com/tvshow/index-2.html',

        #旅游故事会
        'http://travel.hexun.com/travelogue/index.html',
        'http://travel.hexun.com/travelogue/index-1.html'
        ],
        #普通list页正则表达式
        'normalRegex':[
            
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
        #文章，如：
            #http://travel.hexun.com/2009-01-14/113398346.html
            #http://travel.hexun.com/2009-01-14/113398346_3.html
                'itemCollectionName':'Article',
                'regex':'^http://travel\.hexun\.com/\d{4}-\d{2}-\d{2}/\d+(_\d+)*\.html$',
                'priority':600
            }  
        ]
    },

    "peopleSpider":{
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
    },

    "sinaSpider":{
        'allowedDomains':[
        "travel.sina.com.cn",
        "jingdian.travel.sina.com.cn",
        "line.travel.sina.com.cn",
    ],
        'startUrls':[ 
        'http://travel.sina.com.cn/',
        'http://line.travel.sina.com.cn/',

        ],
        #普通list页正则表达式
        'normalRegex':[
            
        {
        #景点，如：http://jingdian.travel.sina.com.cn/151087-yulongxueshan
                'regex':'^http://jingdian\.travel\.sina\.com\.cn/\d+-\w+$',
                'priority':1000
            },
        {
        #城市、景点、资讯、如：
            #http://jingdian.travel.sina.com.cn/223-hanguo/chengshi
            #http://jingdian.travel.sina.com.cn/24507-zhijiage/jingdian
            #http://jingdian.travel.sina.com.cn/24507-zhijiage/zixun
                'regex':'^http://jingdian\.travel\.sina\.com\.cn/\d+-\w+/\w+$',
                'priority':1000
            },
        {
        #列表：美食、娱乐、购物、原创，如：
            #http://jingdian.travel.sina.com.cn/223-hanguo/gonglue/index/2
            #http://jingdian.travel.sina.com.cn/223-hanguo/gonglue/index/4
            #http://jingdian.travel.sina.com.cn/223-hanguo/gonglue/index/3
            #分页：http://jingdian.travel.sina.com.cn/223-hanguo/gonglue/index/1/pn/5
                'regex':'^http://jingdian\.travel\.sina\.com\.cn/\d+-\w+/gonglue/index/\d+(/pn/\d+)?$',
                'priority':1000
            },
        {
        #列表，如：
            #http://travel.sina.com.cn/109/china/ard/cd/list.html
            #http://travel.sina.com.cn/109/hotel/special/list.html
                'regex':'^http://travel\.sina\.com\.cn/.*/list\.html$',
                'priority':1000
            },
        {
        #如：
            #http://travel.sina.com.cn/heilongjiang/
            #http://travel.sina.com.cn/world/North_America/
            #http://travel.sina.com.cn/myshangri-la2/
                'regex':'^http://travel\.sina\.com\.cn(/[\w\-]+)+/$',
                'priority':1000
            },
        {
        #如：
            #酒店：http://travel.sina.com.cn/hotel/index.html
            #机票：http://travel.sina.com.cn/air/index.html
            #http://travel.sina.com.cn/z/beautifulworld7/index.shtml
                'regex':'^http://travel\.sina\.com\.cn/.*/index\.(s)?html$',
                'priority':1000
            },
            
            
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
        #酒店：hotel，如：http://travel.sina.com.cn/hotel/2010-09-20/1441143807.shtml
                'itemCollectionName':'Article1',
                'regex':'^http://travel\.sina\.com\.cn/hotel/\d+-\d+-\d+/\d+(_\d+)?\.shtml$',
                'priority':600
            }, 
        {
        #机票：air，如：http://travel.sina.com.cn/air/2011-02-15/1813152098.shtml
                'itemCollectionName':'Article1',
                'regex':'^http://travel\.sina\.com\.cn/air/\d+-\d+-\d+/\d+(_\d+)?\.shtml$',
                'priority':600
            }, 
        {
        #国内游：china，如：http://travel.sina.com.cn/china/2010-04-07/1406132819.shtml
                'itemCollectionName':'Article1',
                'regex':'^http://travel\.sina\.com\.cn/china/\d+-\d+-\d+/\d+(_\d+)?\.shtml$',
                'priority':600
            },  
        {
        #美食：food，如：http://travel.sina.com.cn/food/2010-02-08/1815127432.shtml
                'itemCollectionName':'Article1',
                'regex':'^http://travel\.sina\.com\.cn/food/\d+-\d+-\d+/\d+(_\d+)?\.shtml$',
                'priority':600
            },  
        {
        #出境游：world，如：http://travel.sina.com.cn/world/2011-09-28/1557162631.shtml
                'itemCollectionName':'Article1',
                'regex':'^http://travel\.sina\.com\.cn/world/\d+-\d+-\d+/\d+(_\d+)?\.shtml$',
                'priority':600
            }, 
        {
        #周边：around，如：http://travel.sina.com.cn/china/ard/2011-04-22/1621155554.shtml
                'itemCollectionName':'Article1',
                'regex':'^http://travel\.sina\.com\.cn/china/ard/\d+-\d+-\d+/\d+(_\d+)?\.shtml$',
                'priority':600
            },
        {
        #资讯：news，如：http://travel.sina.com.cn/news/2009-04-07/161075196.shtml
                'itemCollectionName':'Article1',
                'regex':'^http://travel\.sina\.com\.cn/news/\d+-\d+-\d+/\d+(_\d+)?\.shtml$',
                'priority':600
            },
        
        {
        #资讯：news，如：http://travel.sina.com.cn/news/2009-04-07/161075196.shtml
                'itemCollectionName':'Article1',
                'regex':'^http://travel\.sina\.com\.cn/news/\d+-\d+-\d+/\d+(_\d+)?\.shtml$',
                'priority':600
            }, 


        {
        #线路：line，如：http://line.travel.sina.com.cn/travel/line/69/165675.html
                'itemCollectionName':'Article2',
                'regex':'^http://line\.travel\.sina\.com\.cn/travel/line/\d+/\d+\.html$',
                'priority':600
            },  
        ]
    },

    "lvyou114Spider":{
        'allowedDomains':["www.lvyou114.com" ],
        'startUrls':[                            
            'http://www.lvyou114.com/Youji/index.asp',
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
        #国内游记列表，如：
            #http://www.lvyou114.com/Youji/Class.asp?ClassID=1
            #http://www.lvyou114.com/Youji/class.asp?ClassID=1&page=2
                'regex':'^[Cc]{1}lass\.asp\?[Cc]{1}lassID=\d+(&page=\d+)?$',
                'priority':1000
            },
        {
        #国外游记列表，如：http://www.lvyou114.com/nav/Asia.asp
                'regex':'^\.\./nav/\w+\.asp$',
                'priority':1000
            },
        {
        #国外游记列表，如：http://www.lvyou114.com/nav/Nav_Class.asp?ClassID=73
                'regex':'^Nav_[Cc]{1}lass\.asp\?[Cc]{1}lassID=\d+(&page=\d+)?$',
                'priority':1000
            },
        {
        #国外游记列表，如： http://www.lvyou114.com/youji/Class.asp?ClassID=73
                'regex':'^http://www\.lvyou114\.com/youji/[Cc]{1}lass\.asp\?[Cc]{1}lassID=\d+(&page=\d+)?$',
                'priority':1000
            },
       
        
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            #Article
            {
        #文章，如：http://www.lvyou114.com/Youji/25/25744.html
                'itemCollectionName':'Article',
                'regex':'^\d+/\d+\.html$',
                'priority':600
            },
        {
        #文章，如：http://www.lvyou114.com/Youji/25/25744.html
                'itemCollectionName':'Article',
                'regex':'^http://www\.lvyou114\.com/Youji/\d+/\d+\.html$',
                'priority':600
            }, 
        ]
    },    

     "sohuSpider":{
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
    },

    "9tourSpider":{
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

    "17uSpider":{
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
    },

    "mafengwoSpider":{
        'allowedDomains':["www.mafengwo.cn"],
        'startUrls':[                            
            "http://www.mafengwo.cn",
        'http://www.mafengwo.cn/s/sitemap.html',
        'http://www.mafengwo.cn/mdd/info_list.php',
        'http://www.mafengwo.cn/mdd/travel_list.php',
        ],
        #普通list页正则表达式
        'normalRegex':[    
            {
        #国内外攻略，如：http://www.mafengwo.cn/travel-scenic-spot/mafengwo/11780.html
                'regex':'^/travel-scenic-spot/mafengwo/\d+\.html$',
                'priority':1000
            },
        {
        #国内外攻略分页，如：http://www.mafengwo.cn/mdd/detail.php?mddid=10184&sort=&start=135
                'regex':'^/mdd/detail\.php\?mddid=\d+&sort=&start=\d+$',
                'priority':1000
        },        
        {
        #最新游记列表及分页，如：
            #http://www.mafengwo.cn/mdd/info_list.php
            #http://www.mafengwo.cn/mdd/info_list.php?start=1200
                'regex':'^/mdd/info_list\.php(\?start=\d+)?$',
                'priority':1000
        },
        {
        #资讯列表及分页，如：
            #http://www.mafengwo.cn/mdd/travel_list.php
            #http://www.mafengwo.cn/mdd/travel_list.php?from_time=&type=&start=200
                'regex':'^/mdd/travel_list\.php(\?from_time=&type=&start=\d+)?$',
                'priority':1000
            }
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            {
        #文章，如：http://www.mafengwo.cn/i/741413.html
                'itemCollectionName':'Article',
                'regex':'^http://www\.mafengwo\.cn/i/\d+\.html$',
                'priority':600
            }, 
        {
        #文章，如：http://www.mafengwo.cn/i/751314.html
                'itemCollectionName':'Article',
                'regex':'^/i/\d+\.html$',
                'priority':600
            }, 
        {
        #资讯文章，如：http://www.mafengwo.cn/travel-news/188417.html 
                'itemCollectionName':'Article',
                'regex':'^/travel-news/\d+\.html$',
                'priority':600
            },
        ]
    },

    "bytravelSpider":{
        'allowedDomains':[
        "bytravel.cn",
        "cn.bytravel.cn",
        "as.bytravel.cn",
        "eur.bytravel.cn",
        "usa.bytravel.cn",
        "ca.bytravel.cn",
        "am.bytravel.cn",
        "aftour.bytravel.cn",
        "au.bytravel.cn",
        "shop.bytravel.cn", #特产
        "guangdong.bytravel.cn",
        "beijing.bytravel.cn", 
        "hongkong.bytravel.cn", 
        "taiwan.bytravel.cn",
    ],
        'startUrls':[
            "http://www.bytravel.cn",
        "http://shop.bytravel.cn/",
        "http://shop.bytravel.cn/tc/"
        ],
        #普通list页正则表达式
        'normalRegex':[                           
            {    
        #如：http://ca.bytravel.cn/
                'regex':'^http://\w+\.bytravel\.cn(/)?$',
                'priority':1000
            },
            {
        #如：http://cn.bytravel.cn/v/index113.html
                'regex':'^/v/index\d+\.html$',
                'priority':1000
            },
            {
        #如：http://cn.bytravel.cn/v/2226/
                'regex':'^/v/\d+/$',
                'priority':1000
            },
            {
        #如：http://ca.bytravel.cn/v/199/7/index.html
                'regex':'^/v/\d+/\d+/index\.html$',
                'priority':1000
            },
            {
        #如：
            #http://cn.bytravel.cn/Scenery/tianjinleyuan110/
            #http://cn.bytravel.cn/Scenery/tjbxs/
                'regex':'^/Scenery/\w+/$',
                'priority':1000
            },
            {
        #特产列表，如：http://shop.bytravel.cn/produce/index138.html
                'regex':'^http://shop\.bytravel\.cn/produce/index\d*\.html$',
                'priority':1000
            },
            {
        #特产列表即分页，如：
            #http://shop.bytravel.cn/produce/index495_list.html
            #http://shop.bytravel.cn/produce/index495_list5.html
                'regex':'^index\d*\_list\d*\.html$',
                'priority':1000
            },       
        {
        #特产列表，如：http://shop.bytravel.cn/tc/Silk.html
                'regex':'^http://shop\.bytravel\.cn/tc/\w+\.html$',
                'priority':1000
            },

        {
        #如：http://beijing.bytravel.cn/Scenery/6/
                'regex':'^/Scenery/\d+/$',
                'priority':1000
            },
        {
        #如：http://taiwan.bytravel.cn/Scenery/Kaohsiung/
                'regex':'^/Scenery/[a-zA-Z]+/$',
                'priority':1000
            },
        {
        #如：http://beijing.bytravel.cn/Scenery/jingdong/list/
                'regex':'^/Scenery/\w+/list/$',
                'priority':1000
            },
        {
        #如：http://beijing.bytravel.cn/Scenery/jingdong/2/
                'regex':'^/Scenery/\w+/\d+/$',
                'priority':1000
            } 
        ],
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            {
        #如：http://ca.bytravel.cn/art/142/[dt]blhsyt.html
                'itemCollectionName':'Article1',
                'regex':'^/art/\d+/\[dt\]\w+\.html$',
                'priority':1000
            },
        {
        #如：http://usa.bytravel.cn/art/191/jndjd8ry.html
                'itemCollectionName':'Article1',
                'regex':'^/art/\d+/\w+\.html$',
                'priority':1000
            },
        {
        #如：http://ca.bytravel.cn/art/jnd/jndjsymgzjydpfsm/
                'itemCollectionName':'Article1',
                'regex':'^/art/\w+/\w+/$',
                'priority':1000
            },
        {
        #如：http://ca.bytravel.cn/art/[jn/[jnd]hjadlsbwgmzxz/
                'itemCollectionName':'Article1',
                'regex':'^/art/\[\w+/\[\w+\]\w+/$',
                'priority':1000
            },

        {
        #如：http://beijing.bytravel.cn/Scenery/690/bjsshjbj.html
                'itemCollectionName':'Article1',
                'regex':'^/Scenery/\d+/\w+\.html$',
                'priority':1000
            },
        {
        #如：http://beijing.bytravel.cn/Scenery/762/[dt]zhdlbjjjxsdnlgx.html
                'itemCollectionName':'Article1',
                'regex':'^/Scenery/\d+/\[dt\]\w+\.html$',
                'priority':1000
            },

        {
        #特产，如：http://shop.bytravel.cn/produce2/58546CB39A6C9E7F.html
                'itemCollectionName':'Article2',
                'regex':'^/produce2/\w+\.html$',
                'priority':1000
            },
        {
        #特产，如：http://shop.bytravel.cn/produce/9647535759299EBB/
                'itemCollectionName':'Article2',
                'regex':'^/produce/\w+/$',
                'priority':1000
            }    
        ]
    },

    "QQBlogSpider":{
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
    },

    "lvpingSpider":{
        'allowedDomains':["lvping.com"],
        'startUrls':[
        'http://www.lvping.com/Journals.aspx', #游记总页
        'http://www.lvping.com/Journals.aspx?selecttype=2', #攻略总页
        #目的地
        'http://www.lvping.com/tourism-d110000-china.html', #中国
        'http://www.lvping.com/tourism-d120001-asia.html',
        'http://www.lvping.com/tourism-d120003-oceania.html',
        'http://www.lvping.com/tourism-d120002-europe.html',
        'http://www.lvping.com/tourism-d120006-africa.html',
        'http://www.lvping.com/tourism-d120004-northamerica.html',
        'http://www.lvping.com/tourism-d120005-southamerica.html',
        ],
        #普通list页正则表达式
        'normalRegex':[                       
            {
        #游记总页分页，如：http://www.lvping.com/Journals.aspx?type=0&title=&district=0&IsTitle=T&selecttype=0&orderby=d&pageindex=7
        'regex':r'^/Journals\.aspx\?type=0&title=&district=0&IsTitle=T&selecttype=0&orderby=d&pageindex=\d+$', 
        'priority':200
        }, 
        {
        #攻略总页分页，如：http://www.lvping.com/Journals.aspx?type=0&title=&district=0&IsTitle=T&selecttype=2&orderby=d&pageindex=4
        'regex':r'^/Journals\.aspx\?type=0&title=&district=0&IsTitle=T&selecttype=2&orderby=d&pageindex=\d+$', 
        'priority':200
        },
        {
        #景点列表，如：
            #http://www.lvping.com/attractions-d110000-china.html
            #http://www.lvping.com/attractions-d100047-united-states.html
        'regex':r'^/attractions-d\d+\-[\w\-]+\.html$', 
        'priority':200
        },
        {
        #景点列表，如，美国各地景点，拼音A-Z：http://www.lvping.com/attractions-d100047-pdp1-unitedstates.html
        'regex':r'^/attractions\-d\d+\-pdp\d+\-[\w\-]+\.html$', 
        'priority':200
        },
        {
        #景点列表分页，如：http://www.lvping.com/attractions-d110000-rdp2-china.html
        'regex':r'^/attractions-d\d+\-rdp\d+-[\w\-]+\.html$', 
        'priority':200
        },
        {
        #出行指南，如：http://www.lvping.com/allreviews-d2-shanghai.html
        'regex':r'^/allreviews\-d\d+\-\w+\.html$', 
        'priority':200
        },
        {
        #目的地游玩手册，如：http://www.lvping.com/travel-d2-shanghai:brochure.html
        'regex':r'^/travel\-d\d+\-[\w\-]+:brochure\.html$', 
        'priority':200
        },
        {
        #目的地攻略，如：http://www.lvping.com/journals-d2-s00-p1-g/shanghaijournals.html
        'regex':r'^/journals\-d\d+\-s\d+\-p\d+\-g/[\w\-]+journals\.html$', 
        'priority':200
        },
        {
        #目的地攻略分页，如：http://www.lvping.com/journals-d2-s0-p8-g/shanghai:journals.html
        'regex':r'^/journals\-d\d+\-s\d+\-p\d+\-g/[\w\-]+:journals\.html$', 
        'priority':200
        },
        {
        #目的地游记，如：http://www.lvping.com/journals-d2-s00-p1/shanghaijournals.html
        'regex':r'^/journals\-d\d+\-s\d+\-p\d+/[\w\-]+journals\.html$', 
        'priority':200
        },
        {
        #目的地游记分页，如：http://www.lvping.com/journals-d2-s0-p5/shanghai:journals.html
        'regex':r'^/journals\-d\d+\-s\d+\-p\d+/[\w\-]+:journals\.html$', 
        'priority':200
        },
        
        
        ],
        #item页正则表达式 type对应item存放的数据表名
        'itemRegex':[
        {
            #游记、攻略文章，如：http://www.lvping.com/showjournal-d439-r1334987-journals.html
            'itemCollectionName':'Article',
            'regex':r'^/showjournal\-d\d+-r\d+\-journals\.html$', 
            'priority':1000
        }, 
        {
            #游记、攻略文章，如：http://www.lvping.com/journals/AllSingleJournals.aspx?Writing=1334950
            'itemCollectionName':'Article',
            'regex':r'^/journals/AllSingleJournals\.aspx\?Writing=\d+$', 
            'priority':1000
        },
        {
            #游玩手册里面的主题文章，如：http://www.lvping.com/travel-d2-s16015/shanghai:introduction.html
            'itemCollectionName':'Article',
            'regex':r'^/travel\-d\d+\-s\d+/\w+:\w+\.html$', 
            'priority':1000
        },
        {
            #目的地攻略、游记文章，如：http://www.lvping.com/showjournal-d2-r1334146-detail.html
            'itemCollectionName':'Article',
            'regex':r'^/showjournal\-d\w+\-r\d+\-detail\.html$', 
            'priority':1000
        },
        

        

            {'itemCollectionName':'Note','regex':r'(http://www.lvping.com/)?(travel)+-d\d+-s\w?\d+/\w+:+\w+.*\.html$', 'priority':1000},  #国家介绍 概况、气候等常识
            {'itemCollectionName':'MemberInfo','regex':r'(http://www.lvping.com/)?(members/)+\w+$', 'priority':1}, #用户
            #                                  {'itemCollectionName':'MemberTrack','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/travelmap-public)+$', 'priority':1}, #足迹
            {'itemCollectionName':'MemberFriend','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/friends)+$', 'priority':1}, #好友
            {'itemCollectionName':'MemberNoteList','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/journals)+$', 'priority':1},  #游记MemberNoteList','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/journals)+$', 'priority':1},  #游记
            
            {'itemCollectionName':'Attraction','regex':r'(http://www.lvping.com/)?(attraction_review-)+d\d+-s\d+-[(detail)(attraction)]+\.html$', 'priority':1000}, #景点
            {'itemCollectionName':'Region', 'regex':r'(http://www.lvping.com)?(/tourism-)+d\d+-\w+\.html$', 'priority':300}, #城市景区
        ],
        'imageXpath':['//div[@class="yjDetail cf"]//img/@src']
    },





    #########################################################
    ##            BBS Spider            #
    #########################################################


    'lotourbbsSpider':{
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
    },

      #这个网站可能会出现一些垃圾文章，因为任何版块中帖子的url模式都相同
    'xcarSpider':{
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
    },

    #这个网站看到很多帖子都是垃圾帖子，如：版规、活动结果、后面好几百页
    'sinabbsSpider':{
        'homePage':'http://club.travel.sina.com.cn',
        'allowedDomains':[
            "club.travel.sina.com.cn"
        ],
        'startUrls':[
            'http://club.travel.sina.com.cn/forum-2-1.html', #旅行天下
            'http://club.travel.sina.com.cn/forum-4-1.html', #驴友同行
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                #帖子列表分页，如：http://club.travel.sina.com.cn/forum-2-8.html
                'regex':r'^forum-\d+-\d+\.html$', 
                'priority':700, 
                
            }
        ], 
        #item页正则表达式 itemCollectionName对应item存放的数据表名
        'itemRegex':[
            {
                #帖子文章，如：http://club.travel.sina.com.cn/thread-356808-1-1.html
                'itemCollectionName':'Article',
                'regex':r'^thread\-\d+\-\d+\-\d+\.html$',
                'region':'//div[@class="mainbox threadlist"]',
                'priority':1000
            },
        ]
                
    },
    "jinghuaSpider":{
                     'allowedDomains':[
                                       "www.lvping.com",
                                       "www.go2eu.com",
                                       "www.17u.com",
                                       "bbs.55bbs.com",
                                       ],
                     'startUrls':[
                                  'http://www.lvping.com/Journals.aspx?type=1&pageindex=1', 
                                  'http://www.lvping.com/Journals.aspx?type=2&pageindex=1', #lvping
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=53&filter=digest&page=1', #穷游精选 美国
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=112&filter=digest&page=1', #穷游精选 欧洲
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=14&filter=digest&page=1',#穷游精选 法国
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=12&filter=digest&page=1',#德国
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=13&filter=digest&page=1',#意大利
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=17&filter=digest&page=1',#荷兰比利时
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=16&filter=digest&page=1',#英国
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=19&filter=digest&page=1',#奥地利
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=18&filter=digest&page=1',#西班牙
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=15&filter=digest&page=1',#瑞士
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=26&filter=digest&page=1',#希腊
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=58&filter=digest&page=1',#亚洲各国
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=57&filter=digest&page=1',#日本韩国
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=106&filter=digest&page=1',#泰国
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=108&filter=digest&page=1',#新马泰
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=107&filter=digest&page=1',#柬埔寨
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=110&filter=digest&page=1',#菲律宾
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=111&filter=digest&page=1',#印尼
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=103&filter=digest&page=1',#印度
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=102&filter=digest&page=1',#尼泊尔
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=104&filter=digest&page=1',#马尔代夫
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=52&filter=digest&page=1',#香港
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=51&filter=digest&page=1',#国内
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=53&filter=digest&page=1',#美国
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=54&filter=digest&page=1',#加拿大
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=55&filter=digest&page=1',#拉美
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=56&filter=digest&page=1',#澳大利亚
                                  'http://www.go2eu.com/bbs/forumdisplay.php?fid=83&filter=digest&page=1',#新西兰
                                  'http://www.17u.com/blog/best/1',#17u.com
                                  'http://bbs.55bbs.com/forumdisplay.php?fid=34&filter=digest&page=1',#55bbs
                                  ],
                     #普通list页正则表达式
                     'normalRegex':[
                                    #lvping
                                    {
                                     'regex':r'/Journals\.aspx\?type=[12]+&title=&district=0&IsTitle=T&selecttype=0&orderby=[rd]+&pageindex=\d+$', 
                                     'region':'//form[@id="newMasterForm"]/div[5]/div[2]/div[3]/div[3]',
                                     'priority':1,
                                     },
                                    #go2eu
                                    {
                                     'regex':r'forumdisplay\.php\?fid=\d+&filter=digest&page=\d+$',
                                     'region':'//body/div[6]/div[4]/div',
                                     'priority':1, 
                                     },
                                    #17u
                                    {
                                     'regex':r'/blog/best/\d+$',
                                     'region':'//div[@id="pageList"]/div',
                                     'priority':1, 
                                     },
                                    #55bbs
                                    {
                                     'regex':r'forumdisplay\.php\?fid=34&filter=digest&page=\d+$', 
                                     'region':'//div[@id="list_left"]/div[1]/div[1]',
                                     'priority':1,
                                     },
                                    ],
                     #item页正则表达式 itemCollectionName对应item存放的数据表名
                     'itemRegex':[
                                  #lvping
                                  {
                                   'itemCollectionName':'Article',
                                   'regex':r'(/showjournal\-d\d+-r\d+\-journals\.html)|(/journals/AllSingleJournals\.aspx\?Writing=\d+)|(travel\-d\d+\-s\d+/\w+:\w+\.html)|(/showjournal\-d\w+\-r\d+\-detail\.html)',
                                   'region':'//div[@id="yjDetail"]',
                                   'priority':1000
                                   },
                                  #go2eu
                                  {
                                   'itemCollectionName':'BBSArticle',
                                   'regex':r'viewthread\.php\?tid=\d+&extra=page[(=)|(%3D)]+\d+[(&)|(%26)]+amp[(;)|(%3B)]+filter[(=)|(%3D)]+digest$',
                                   'region':'//div/form/table',
                                   'priority':1000
                                   },
                                  #17u
                                  {
                                   'itemCollectionName':'BBSArticle',
                                   'regex':r'/blog/article/\d+\.html$',
                                   'region':'//div[@id="major"]/table',
                                   'priority':1000
                                   },
                                  #55bbs
                                  {
                                   'itemCollectionName':'BBSArticle',
                                   'regex':r'thread-\d+-1-\d+\.html$',
                                   'region':'//div/form/table',
                                   'priority':1000
                                   },
                                  ]
                     },
                
    "onegreenSpider":{
                     'allowedDomains':[
                                       "www.onegreen.net",
                                       ],
                     'startUrls':[
                                  'http://www.onegreen.net/maps/List/List_711.html',
#                                  'http://www.onegreen.net/maps/List/List_1167.html',
#                                  'http://www.onegreen.net/maps/List/List_712.html',
#                                  'http://www.onegreen.net/maps/List/List_747.html',
#                                  'http://www.onegreen.net/maps/List/List_748.html',
#                                  'http://www.onegreen.net/maps/List/List_749.html',
#                                  'http://www.onegreen.net/maps/List/List_750.html',
#                                  'http://www.onegreen.net/maps/List/List_751.html',
#                                  'http://www.onegreen.net/maps/List/List_752.html',
#                                  'http://www.onegreen.net/maps/List/List_753.html',
#                                  'http://www.onegreen.net/maps/List/List_754.html',
#                                  'http://www.onegreen.net/maps/List/List_755.html',
#                                  'http://www.onegreen.net/maps/List/List_756.html',
#                                  'http://www.onegreen.net/maps/List/List_757.html',
#                                  'http://www.onegreen.net/maps/List/List_758.html',
#                                  'http://www.onegreen.net/maps/List/List_759.html',
#                                  'http://www.onegreen.net/maps/List/List_760.html',
#                                  'http://www.onegreen.net/maps/List/List_761.html',
#                                  'http://www.onegreen.net/maps/List/List_762.html',
#                                  'http://www.onegreen.net/maps/List/List_763.html',
#                                  'http://www.onegreen.net/maps/List/List_764.html',
#                                  'http://www.onegreen.net/maps/List/List_765.html',
#                                  'http://www.onegreen.net/maps/List/List_766.html',
#                                  'http://www.onegreen.net/maps/List/List_767.html',
#                                  'http://www.onegreen.net/maps/List/List_768.html',
#                                  'http://www.onegreen.net/maps/List/List_769.html',
#                                  'http://www.onegreen.net/maps/List/List_770.html',
#                                  'http://www.onegreen.net/maps/List/List_771.html',
#                                  'http://www.onegreen.net/maps/List/List_772.html',
#                                  'http://www.onegreen.net/maps/List/List_1177.html',#交通图
                                  ],
                     #普通list页正则表达式
                     'normalRegex':[
                                    {
                                     'regex':r'/maps/ShowClass\.asp\?ClassID=\d+&page=\d+$',
                                     'region':'//table[1]//table//tr[2]/td/div',
                                     'priority':1,
                                     },
                                    ],
                     #item页正则表达式 itemCollectionName对应item存放的数据表名
                     'itemRegex':[
                                  {
                                   'itemCollectionName':'ImageItem',
                                   'regex':r'/maps/HTML/\d+\.html$',
                                   'region':'//table[1]//table//tr[2]/td/table',
                                   'priority':1000
                                   },
                                  ]
                     },
    
        
        
           
    
            #------------------------------------------------------------------------------------------------------------------------------------
            "bbsSpider":{
                     'homePage':'http://www.go2eu.com/bbs/',  
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
                     'homePage':'http://www.go2eu.com/bbs/',  
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
#                                #测试
#                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=98',

                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=12', #德国
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=14', #法国
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=13', #意大利
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=17', #荷比卢
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=18', #西班牙葡萄牙
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=19', #奥地利
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=16', #英国
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=15', #瑞士
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=26', #希腊土耳其
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=25', #北欧
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=24', #东欧
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=58', #东南亚
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=57', #东亚
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=59', #西亚南亚
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=51', #中国
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=52', #港澳台
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=53', #美国
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=54', #加拿大
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=55', #拉美
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=56', #澳大利亚
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=83', #新西兰
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=86', #埃及
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=60', #非洲
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=94', #游轮
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=3', #签证
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=1', #多国
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=62', #廉航
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=79', #交通
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=33', #自驾
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=80', #购物
                                'http://www.go2eu.com/bbs/forumdisplay.php?fid=100', #银联
                               ],
                
                 #普通list页正则表达式
                 'normalRegex':[
                                {'regex':r'forumdisplay.php\?fid=\d+', 'priority':700, 'region':'//div/div[@class="pages"]'}, #列表后续页，在板块页中找 &page=\d+$
                               ],
                 #item页正则表达式 itemCollectionName对应item存放的数据表名
                 'itemRegex':[
                              {
                               'itemCollectionName':'BBSArticle',
                               'regex':r'(viewthread\.php\?tid=\d+&extra=page.{1,4}\d+)|(http://www\.go2eu\.com/bbs/viewthread\.php\?action=printable&tid=.*)',
                               'itemPrintPageFormat':r'http://www.go2eu.com/bbs/viewthread.php?action=printable&tid=%s',
                               'itemTidRegex':r'tid=(\d+)',
                               'region':'//div/form/table',
                               'priority':1000
                               },
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
#            'http://bbs.lvye.cn/forum-haiwai-1.html'#海外
        ],
        #普通list页正则表达式
        'normalRegex':[
            {
                'regex':r'forum-\d+-\d+.html$', 
                'priority':700, 
                'region':'//div[@class="pg"]'
            }, #帖子列表页
            {    
                #海外版帖子列表分页，如：http://bbs.lvye.cn/forum-haiwai-9.html
                'regex':r'^http://bbs\.lvye\.cn/forum\-haiwai\-\d+\.html$', 
                'priority':700, 
                'region':'//div[@class="pg"]'
            }, #帖子列表页
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
                
                
}
