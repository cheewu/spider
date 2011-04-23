# -*- coding: utf-8 -*-

spiderConfig = {
                "daodaoSpider":{
                     'allowedDomains':["daodao.com"],
                     'startUrls':['http://www.daodao.com/Attractions-g294211-Activities-China.html'],
                     #普通list页正则表达式
                     'normalRegex':[
                                    {'regex':r'Tourism-g\d+-.*-Vacations\.html$', 'priority':10},
                                    {'regex':r'Attractions-g\d+-Activities-.*\.html$', 'priority':50},
                                    {'regex':r'Tourism-g\d+-c\d+-[^n].*\.html((\?pg=\d+)?|(\?kw=.*&st=8))$', 'priority':50} #包括游记列表、标签
                                    ],
                     #item页正则表达式
                     'itemRegex':[{'type':'Attraction','regex':r'Attraction_Review-g\d+-.*-Reviews-.*\.html$', 'priority':600},  #AttractionItem
                                  {'type':'Note','regex':r'Tourism-g\d+-c\d+-n\d+.*\.html$', 'priority':500},              #NoteItem
                                  {'type':'CommonSense','regex':r'Changshi-g\d+-.*\.html$', 'priority':500}                       #CommonSenseItem
                                  ]
                     },
                "lvpingSpider":{
                     'allowedDomains':["lvping.com"],
                     'startUrls':[
                                  'http://www.lvping.com/NorthAmericaNavigation.aspx',
                                  'http://www.lvping.com/EuropeNavigation.aspx',
                                  'http://www.lvping.com/AsiaNavigation.aspx',
                                  'http://www.lvping.com/ChinaNavigation.aspx',
                                  'http://www.lvping.com/OceaniaNavigation.aspx',
                                  'http://www.lvping.com/southAmericaNavigation.aspx',
                                  'http://www.lvping.com/AfricaNavigation.aspx',

                                  #游记攻略
                                  'http://www.lvping.com/Journals.aspx?type=1',
                                  'http://www.lvping.com/Journals.aspx?selecttype=2'
                                  ],
                     #普通list页正则表达式
                     'normalRegex':[
                                    {'regex':r'(http://www.lvping.com/)?(tourism-)+(g\d-)+\w\.html$', 'priority':10}, #国家
                                    {'regex':r'(http://www.lvping.com/)?(tourism-)+(d\d-)+\w+\.html$', 'priority':50}, #城市景区
                                    {'regex':r'(http://www.lvping.com/)?(attractions-)+(d\d-)+\w\.html$', 'priority':50}, #景点列表
                                    {'regex':r'(http://www.lvping.com/)?(journals-)+(d\d)+(-s\d)+(-p\d)+(-g/\w)+\.html$', 'priority':50}, #攻略列表
                                    {'regex':r'(http://www.lvping.com)?(/members/)+(\w/)+journals$', 'priority':50}# 会员游记列表
                                    ],
                     #item页正则表达式
                     'itemRegex':[{'type':'CommonSense','regex':r'(http://www.lvping.com/)?(travel-)+(d\d-)+\w+[:]\w+\.html$', 'priority':600},  #国家介绍 概况、气候等常识
                                  {'type':'Note','regex':r'(http://www.lvping.com/)?(travel-)+(d1-)+(s\d)+/\w:\w\.html$', 'priority':500}, #短文攻略(类别 内容 目的地)
                                  {'type':'Attraction','regex':r'(http://www.lvping.com/)?(attraction_review-)+(s\d-)+detail\.html$', 'priority':500}, #景点
                                  {'type':'Note','regex':r'(http://www.lvping.com/)?(showjournal-)+(d\d-)+(r\d-)+(-journals)+\.html$', 'priority':600}, #攻略 作者 发表时间 浏览次数 评论次数
                                  {'type':'MemberInfo','regex':r'(http://www.lvping.com/)?(members/)+\w+$', 'priority':600}, #用户
                                  {'type':'MemberTrack','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/travelmap-public)+$', 'priority':600}, #足迹
                                  {'type':'MemberFriend','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/friends)+$', 'priority':600}, #好友
                                  {'type':'MemberNoteList','regex':r'(http://www.lvping.com/)?(members/)+(\w)+(/journals)+$', 'priority':600}  #游记
                                  ]
                     }
}