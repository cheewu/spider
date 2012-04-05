# -*- coding: utf-8 -*-
from scrapy.cmdline import execute
from zijiyou.common.extractText import Extracter
from zijiyou.spiders.offlineCrawl.parse import Parse
import sys

#解析
def beginparse(argv=None):
    if argv == None:
        argv = sys.argv
        argv = argv[1:]
        print argv
    if len(argv) > 0:
        p = Parse()
        p.parse(spiderName = argv)

def beginspider(argv=None): 
    if argv == None:
        argv = sys.argv
        argv = argv[1:]
        print argv
    if len(argv) >= 1:
        execute(argv=['scrapy','crawl',argv[0]])
    else:
        print '必须提供至少一个爬虫的名字'
    
if __name__ == '__main__':
    beginparse()
