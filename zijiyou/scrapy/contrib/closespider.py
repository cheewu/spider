"""CloseSpider is an extension that forces spiders to be closed after certain
conditions are met.

See documentation in docs/topics/extensions.rst
"""

from collections import defaultdict

from twisted.internet import reactor
from twisted.python import log as txlog
from scrapy.xlib.pydispatch import dispatcher

from scrapy import signals, log
from scrapy.project import crawler
from scrapy.conf import settings

class CloseSpider(object):

    def __init__(self):
        self.timeout = settings.getint('CLOSESPIDER_TIMEOUT')
        self.itempassed = settings.getint('CLOSESPIDER_ITEMPASSED')
        self.pagecount = settings.getint('CLOSESPIDER_PAGECOUNT')
        self.errorcount = settings.getint('CLOSESPIDER_ERRORCOUNT')

        self.errorcounts = defaultdict(int)
        self.pagecounts = defaultdict(int)
        self.counts = defaultdict(int)
        self.tasks = {}

        if self.errorcount:
            txlog.addObserver(self.catch_log)
        if self.pagecount:
            dispatcher.connect(self.page_count, signal=signals.response_received)
        if self.timeout:
            dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        if self.itempassed:
            dispatcher.connect(self.item_passed, signal=signals.item_passed)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def catch_log(self, event):
        if event.get('logLevel') == log.ERROR:
            spider = event.get('spider')
            if spider:
                self.errorcounts[spider] += 1
                if self.errorcounts[spider] == self.errorcount:
                    crawler.engine.close_spider(spider, 'closespider_errorcount')

    def page_count(self, response, request, spider):
        self.pagecounts[spider] += 1
        if self.pagecounts[spider] == self.pagecount:
            crawler.engine.close_spider(spider, 'closespider_pagecount')

    def spider_opened(self, spider):
        self.tasks[spider] = reactor.callLater(self.timeout, \
            crawler.engine.close_spider, spider=spider, \
            reason='closespider_timeout')

    def item_passed(self, item, spider):
        self.counts[spider] += 1
        if self.counts[spider] == self.itempassed:
            crawler.engine.close_spider(spider, 'closespider_itempassed')

    def spider_closed(self, spider):
        self.counts.pop(spider, None)
        self.pagecounts.pop(spider, None)
        self.errorcounts.pop(spider, None)
        tsk = self.tasks.pop(spider, None)
        if tsk and tsk.active():
            tsk.cancel()
