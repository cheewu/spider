# -*- coding: utf-8 -*-

baseSeSpider={
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
                     }                     