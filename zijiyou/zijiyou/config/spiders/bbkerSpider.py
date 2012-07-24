# -*- coding: utf-8 -*-
bbkerSpider={
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
                   }