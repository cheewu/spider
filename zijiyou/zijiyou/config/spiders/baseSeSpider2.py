# -*- coding: utf-8 -*-
baseSeSpider2={
               
                     'allowedDomains':[],
                     'startUrls':['http://blog.soso.com'],
                     'seUrlFormat':[
                                    {
                                     #搜索引擎名称
                                     'seName':'sosoBlog',
                                     #搜素格式 
                                     'format':'http://blog.soso.com/qz.q?sc=qz&pid=qz.s.res&ty=blog&st=r&op=blog.blog&sd=0&w=%s&pg=%s',#搜索格式
                                     #输入编码
                                     'encode':'GBK',
                                     #搜素结果中，目标页的url的xpath
                                     'resultItemLinkXpath':'//div[@id="result"]/ol/li/h3/a/@href',
                                     #搜素结果中搜素结果页数xpath
                                     'totalRecordXpath':'//div[@id="sNum"]/text()',
                                     #搜素结果中搜素结果页数
                                     'totalRecordRegex':r'[\d|,]+',
                                     #搜素引擎下一页的格式
                                     'nextPagePattern':'http://blog.soso.com/qz.q?w=keyWord&sc=qz&ty=blog&sd=0&st=r&cid=&op=blog.blog&pid=qz.s.res&pg=pageNum',
                                     #搜素引擎域
                                     'homePage':'http://blog.soso.com'
                                     },
#                                    {
#                                     #搜索引擎名称
#                                     'seName':'qihoo',
#                                     #搜素格式
#                                     'format':'http://www.qihoo.com/wenda.php?kw=%s&do=search&src=wenda_search&area=0&page=%s',#搜索格式
#                                     #输入编码
#                                     'encode':'GBK',
#                                     #搜素结果中，目标页的url的xpath
#                                     'resultItemLinkXpath':'//body/table//tr/td[2]/div/table//tr/td',
#                                     #搜素结果中搜素结果页数xpath
#                                     'totalRecordXpath':'//table//tr/td[2]/table//tr/td/div/em/text()',
#                                     #搜素结果中搜素结果页数
#                                     'totalRecordRegex':r'[\d|,]+',
#                                     #搜素引擎下一页的格式
#                                     'nextPagePattern':'http://www.qihoo.com/wenda.php?kw=%s&do=search&src=wenda_search&area=0&page=%s',
#                                     #搜素引擎域
#                                     'homePage':'http://www.qihoo.com'
#                                     }
                                    ],
                    'seXpath':{
                               "sosoBlog":{
                                           },
                                "qihoo":{
                                        }
                               },
                     #普通list页正则表达式
                     'normalRegex':[],
                     #item页正则表达式 itemCollectionName对应item存放的数据表名
                     'itemRegex':[]
                     
               
               
               }  
 
                 