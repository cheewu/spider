# -*- coding: utf-8 -*-
Spider55bbs={
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
            
                     }