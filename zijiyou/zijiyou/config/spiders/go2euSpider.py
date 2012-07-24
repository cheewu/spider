# -*- coding: utf-8 -*-
go2euSpider={
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
                    
                }