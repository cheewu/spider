# -*- coding: utf-8 -*-
from zijiyou.spiders.offlineCrawl.parse import Parse


#from scrapy.cmdline import execute
#
if __name__ == "__main__":
    p = Parse(isOffline=True)
    p.parse(spiderName=['yahooSpider', 'lvrenSpider', 'sozhenSpider', '21cnSpider' ,'meishiSpider' ,'hexunSpider' ,'peopleSpider' ,'sinaSpider', 'lvyou114Spider', 'sohuSpider', '9tourSpider', 'lotourSpider' ,'17uSpider', 'mafengwoSpider','bytravelSpider', 'QQBlogSpider', 'lvpingSpider', 'lotourbbsSpider', 'xcarSpider', 'sinabbsSpider', '55bbsSpider' ,'go2euSpider', 'lvyeSpider' ])

#import urllib
#t="台湾 游记"
#encodeWords = urllib.quote(t.encode('GBK'))
#print encodeWords

