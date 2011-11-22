# -*- coding: utf-8 -*-
#from scrapy.cmdline import execute
#from zijiyou.common.extractText import Extracter
from zijiyou.spiders.offlineCrawl.parse import Parse
#import re
#from zijiyou.spiders.offlineCrawl.parse import Parse
#解析
#if __name__ == "__main__":
#    p = Parse(isOffline=True)
#    p.parse(spiderName=['daodaoSpider'])#,'lvpingSpider','mafengwoSpider','hexunSpider','go2euSpider'

#运行爬虫
#if __name__ == "__main__":
#    execute(argv=['scrapy','crawl','daodaoSpider'])

#'17uSpider','21cnSpider','55bbsSpider','bbkerSpider','bytravelSpider','daodaoSpider',
#'go2euSpider','hexunSpider','lotourSpider','lotourbbsSpider','lvpingSpider','lvrenSpider',
#'lvyeSpider','lvyou114Spider','mafengwoSpider','meishiSpider','peopleSpider','QQBlogSpider',
# 'sinaSpider','sinabbsSpider','sohuSpider','sozhenSpider','xcarSpider','yahooSpider','baseSeSpider','bbsSpider2'

#正文抽取
#ex = Extracter()
#html=''
#f = open('/home/shiym/data/travel')
#for p in f:
#    html += p
#title,pd,content = ex.doExtract(html,threshold=0.4)
#print title,pd
#print '===================='
#print content

#解析
'''

'''
p = Parse()
p.parse(spiderName=['17uSpider','sozhenSpider','sohuSpider','21cnSpider','55bbsSpider','bbkerSpider','bytravelSpider','daodaoSpider','go2euSpider','hexunSpider','lotourSpider','lotourbbsSpider','lvpingSpider',
                    'lvrenSpider','lvyeSpider','lvyou114Spider','mafengwoSpider','meishiSpider','peopleSpider','QQBlogSpider','sinaSpider','sinabbsSpider',
                    'xcarSpider','yahooSpider'])

#t = u'2011年08月02日 18：22'
#t = str(t)
#r = r'(\d{4}[年-]+\d{1,2}[月-]+\d{1,2}[日]*)'
#t = re.search(r, t)
#if t:
#    print t.group(1)

