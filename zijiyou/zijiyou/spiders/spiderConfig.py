# -*- coding: utf-8 -*-

spiderConfig = {
                "baseSeSpider":{
                     'allowedDomains':[],
                     'startUrls':['http://www.baidu.com'],
                     'seUrlFormat':[{'seName':'sosoBlog',
                                     'format':'http://blog.soso.com/qz.q?sc=qz&pid=qz.s.res&ty=blog&st=r&op=blog.blog&sd=0&w=%s&pg=%s',#搜索格式
                                     'sePageNum':5,
                                     'encode':'GBK',
                                     'resultItemLinkXpath':'//div[2]/div[2]/div[2]/ol/li/a/@href',
                                     'nextPageLinkXpath':'//div[@class="page"]/div[@class="pg"]/a/@href',
                                     'nextPagePattern':'http://blog.soso.com/qz.q?w=keyWord&sc=qz&ty=blog&sd=0&st=r&cid=&op=blog.blog&pid=qz.s.res&pg=pageNum',#无法通过xpath获得js动态生成的下一页区域，使用模板
                                     'homePage':'http://blog.soso.com'                                  
                                     }],
                    'seXpath':{
                               "sosoBlog":{
                                    r'title':r'//div[@id="main"]/h3/text()',
                                    r'date':r'//div[@id="main"]/text()[2]',
                                    r'content':r'//div[@id="main"]',
                                    r'originUrl':r'//div[@id="header"]/a/text()'
                                    }
                               },
                     #普通list页正则表达式
                     'normalRegex':[],
                     #item页正则表达式 type对应item存放的数据表名
                     'itemRegex':[]
                     },
                "daodaoSpider":{
                     'allowedDomains':["daodao.com"],
                     'startUrls':['http://www.daodao.com/Attractions-g294211-Activities-China.html'],
                     #普通list页正则表达式
                     'normalRegex':[
                                    {'regex':r'Tourism-g\d+-.*-Vacations\.html$', 'priority':10},
                                    {'regex':r'Attractions-g\d+-Activities-.*\.html$', 'priority':50},
                                    {'regex':r'Tourism-g\d+-c\d+-[^n].*\.html((\?pg=\d+)?|(\?kw=.*&st=8))$', 'priority':50} #包括游记列表、标签
                                    ],
                     #item页正则表达式 type对应item存放的数据表名
                     'itemRegex':[{'type':'Attraction','regex':r'Attraction_Review-g\d+-.*-Reviews-.*\.html$', 'priority':600},  #AttractionItem
                                  {'type':'Note','regex':r'Tourism-g\d+-c\d+-n\d+.*\.html$', 'priority':500},              #NoteItem
                                  {'type':'CommonSense','regex':r'Changshi-g\d+-.*\.html$', 'priority':500}                       #CommonSenseItem
                                  ]
                     },
                "lvpingSpider":{
                     'allowedDomains':["lvping.com"],
                     'startUrls':[
#                                  'http://www.lvping.com/NorthAmericaNavigation.aspx',
#                                  'http://www.lvping.com/EuropeNavigation.aspx',
#                                  'http://www.lvping.com/AsiaNavigation.aspx',
#                                  'http://www.lvping.com/ChinaNavigation.aspx',
                                  'http://www.lvping.com/attraction_review-d308-s12565-detail.html',#测试
                                  'http://www.lvping.com/attraction_review-d1-s229-attraction.html',#测试
#                                  'http://www.lvping.com/OceaniaNavigation.aspx',
#                                  'http://www.lvping.com/southAmericaNavigation.aspx',
#                                  'http://www.lvping.com/AfricaNavigation.aspx',
#
#                                  #游记攻略
#                                  'http://www.lvping.com/Journals.aspx?type=1',
#                                  'http://www.lvping.com/Journals.aspx?selecttype=2',
                                  ],
                     #普通list页正则表达式
                     'normalRegex':[
#                                    {'regex':r'(http://www.lvping.com/)?(tourism)+-g\d+-\w+\.html$', 'priority':200}, #国家
#                                    {'regex':r'(http://www.lvping.com/)?(tourism-)+d\d+-\w+\.html$', 'priority':300}, #城市景区
#                                    {'regex':r'(http://www.lvping.com/)?(attractions-)+d\d+-\w+\.html$', 'priority':400}, #景点列表
#                                    {'regex':r'(http://www.lvping.com/)?(attractions-)+d\d+-s\d+-[r]+\w+\d+/\w+:\w+\.html$', 'priority':500}, #景点列表
#                                    {'regex':r'(http://www.lvping.com/)?(attractions-)+g\d+-\w+\.html$', 'priority':400}, #景点列表
#                                    {'regex':r'(http://www.lvping.com/)?(attractions-)+g\d+-[r]+\w+\d+-\w+\.html$', 'priority':450}, #景点列表
#                                    
#                                    {'regex':r'(http://www.lvping.com/)?(journals-)+d\d+-s\d+-p\d+-g/\w+\.html$', 'priority':1}, #攻略列表
#                                    {'regex':r'(http://www.lvping.com)?(/members/)+(\w/)+journals$', 'priority':1},# 会员游记列表
#                                    {'regex':r'(http://www.lvping.com)?/Journals.aspx\?type=1.*selecttype=0.*', 'priority':1},# 精品游记列表
#                                    {'regex':r'(http://www.lvping.com)?/Journals.aspx\?.*selecttype=2.*', 'priority':1}# 攻略列表
                                    ],
                     #item页正则表达式 type对应item存放的数据表名
                     'itemRegex':[
#                                  {'type':'CommonSense','regex':r'(http://www.lvping.com/)?(travel)+-d\d+-s\w?\d+/\w+:+\w+.*\.html$', 'priority':1},  #国家介绍 概况、气候等常识
#                                  {'type':'Note','regex':r'(http://www.lvping.com/)?(travel-)+d1-+s\d+/\w+:\w+\.html$', 'priority':1}, #短文攻略(类别 内容 目的地)
#                                  {'type':'Note','regex':r'(http://www.lvping.com/)?(showjournal-)+d\d+-r\d+-journals+\.html$', 'priority':1}, #攻略 作者 发表时间 浏览次数 评论次数
#                                  {'type':'Note','regex':r'(http://www.lvping.com/)?journals/AllSingleJournals.aspx\?Writing=\d+', 'priority':1}, #第二种攻略游记情况 http://www.lvping.com/journals/AllSingleJournals.aspx?Writing=1322380
#                                  {'type':'MemberInfo','regex':r'(http://www.lvping.com/)?(members/)+\w+$', 'priority':1}, #用户
#                                  {'type':'MemberTrack','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/travelmap-public)+$', 'priority':1}, #足迹
#                                  {'type':'MemberFriend','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/friends)+$', 'priority':1}, #好友
#                                  {'type':'MemberNoteList','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/journals)+$', 'priority':1},  #游记
                                  
                                  {'type':'Attraction','regex':r'(http://www.lvping.com/)?(attraction_review-)+d\d+-s\d+-[(detail)(attraction)]+\.html$', 'priority':1000} #景点
                                  ]
                     }
}