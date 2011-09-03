# -*- coding: utf-8 -*-

from zijiyou.spiders.offlineCrawl.parse import Parse
p=Parse(isOffline=True)
p.parse(spiderName=['baseSeSpider','sozhenSpider','bbkerSpider','mafengwoSpider','lvyou114Spider'])