# -*- coding: utf-8 -*-
lvyeSpider={
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
            
                     }