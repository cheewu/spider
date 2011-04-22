# -*- coding: utf-8 -*-

spiderConfig = {
                "daodaoSpider":{
                     'allowedDomains':["daodao.com"],
                     'startUrls':['http://www.daodao.com/Lvyou'],
                     #普通页正则表达式
                     'normalRegex':[
                                    {'regex':r'Tourism-g\d+-.*-Vacations\.html$', 'priority':10},
                                    {'regex':r'Attractions-g\d+-Activities-.*\.html$', 'priority':50},
                                    {'regex':r'Tourism-g\d+-c\d+-[^n].*\.html((\?pg=\d+)?|(\?kw=.*&st=8))$', 'priority':50} #包括游记列表、标签
                    ],
                     #item页正则表达式
                     'itemRegex':[{'regex':r'Attraction_Review-g\d+-.*-Reviews-.*\.html$', 'priority':500},  #AttractionItem
                                  {'regex':r'Tourism-g\d+-c\d+-n\d+.*\.html$', 'priority':500},              #NoteItem
                                  {'regex':r'Changshi-g\d+-.*\.html$', 'priority':500}                       #CommonSenseItem
                    ]
                }
}