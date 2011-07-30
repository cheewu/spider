"""This module implements the Scraper component which parses responses and
extracts information from them"""

from twisted.python.failure import Failure
from twisted.internet import defer

from scrapy.utils.defer import defer_result, defer_succeed, parallel, iter_errback
from scrapy.utils.spider import iterate_spider_output
from scrapy.utils.misc import load_object
from scrapy.utils.signal import send_catch_log, send_catch_log_deferred
from scrapy.exceptions import IgnoreRequest, DropItem
from scrapy import signals
from scrapy.http import Request, Response
from scrapy.item import BaseItem
from scrapy.core.spidermw import SpiderMiddlewareManager
from scrapy import log
from scrapy.stats import stats


class SpiderInfo(object):
    """Object for holding data of the responses being scraped"""

    MIN_RESPONSE_SIZE = 1024

    def __init__(self, max_active_size=5000000):
        self.max_active_size = max_active_size
        self.queue = []
        self.active = set()
        self.active_size = 0
        self.itemproc_size = 0
        self.closing = None

    def add_response_request(self, response, request):
        deferred = defer.Deferred()
        self.queue.append((response, request, deferred))
        if isinstance(response, Response):
            self.active_size += max(len(response.body), self.MIN_RESPONSE_SIZE)
        else:
            self.active_size += self.MIN_RESPONSE_SIZE
        return deferred

    def next_response_request_deferred(self):
        response, request, deferred = self.queue.pop(0)
        self.active.add(response)
        return response, request, deferred

    def finish_response(self, response):
        self.active.remove(response)
        if isinstance(response, Response):
            self.active_size -= max(len(response.body), self.MIN_RESPONSE_SIZE)
        else:
            self.active_size -= self.MIN_RESPONSE_SIZE

    def is_idle(self):
        return not (self.queue or self.active)

    def needs_backout(self):
        return self.active_size > self.max_active_size

class Scraper(object):

    def __init__(self, engine, settings):
        self.sites = {}
        self.spidermw = SpiderMiddlewareManager.from_settings(settings)
        itemproc_cls = load_object(settings['ITEM_PROCESSOR'])
        self.itemproc = itemproc_cls.from_settings(settings)
        self.concurrent_items = settings.getint('CONCURRENT_ITEMS')
        self.engine = engine

    @defer.inlineCallbacks
    def open_spider(self, spider):
        """Open the given spider for scraping and allocate resources for it"""
        assert spider not in self.sites, "Spider already opened: %s" % spider
        self.sites[spider] = SpiderInfo()
        yield self.itemproc.open_spider(spider)

    def close_spider(self, spider):
        """Close a spider being scraped and release its resources"""
        assert spider in self.sites, "Spider not opened: %s" % spider
        site = self.sites[spider]
        site.closing = defer.Deferred()
        site.closing.addCallback(self.itemproc.close_spider)
        self._check_if_closing(spider, site)
        return site.closing

    def is_idle(self):
        """Return True if there isn't any more spiders to process"""
        return not self.sites

    def _check_if_closing(self, spider, site):
        if site.closing and site.is_idle():
            del self.sites[spider]
            site.closing.callback(spider)

    def enqueue_scrape(self, response, request, spider):
        site = self.sites.get(spider, None)
        if site is None:
            return
        dfd = site.add_response_request(response, request)
        def finish_scraping(_):
            site.finish_response(response)
            self._check_if_closing(spider, site)
            self._scrape_next(spider, site)
            return _
        dfd.addBoth(finish_scraping)
        dfd.addErrback(log.err, 'Scraper bug processing %s' % request, \
            spider=spider)
        self._scrape_next(spider, site)
        return dfd

    def _scrape_next(self, spider, site):
        while site.queue:
            response, request, deferred = site.next_response_request_deferred()
            self._scrape(response, request, spider).chainDeferred(deferred)

    def _scrape(self, response, request, spider):
        """Handle the downloaded response or failure trough the spider
        callback/errback"""
        assert isinstance(response, (Response, Failure))

        dfd = self._scrape2(response, request, spider) # returns spiders processed output
        dfd.addErrback(self.handle_spider_error, request, spider)
        dfd.addCallback(self.handle_spider_output, request, response, spider)
        return dfd

    def _scrape2(self, request_result, request, spider):
        """Handle the diferent cases of request's result been a Response or a
        Failure"""
        if not isinstance(request_result, Failure):
            return self.spidermw.scrape_response(self.call_spider, \
                request_result, request, spider)
        else:
            # FIXME: don't ignore errors in spider middleware
            dfd = self.call_spider(request_result, request, spider)
            return dfd.addErrback(self._check_propagated_failure, \
                request_result, request, spider)

    def call_spider(self, result, request, spider):
        dfd = defer_result(result)
        dfd.addCallbacks(request.callback or spider.parse, request.errback)
        return dfd.addCallback(iterate_spider_output)

    def handle_spider_error(self, _failure, request, spider, propagated_failure=None):
        referer = request.headers.get('Referer', None)
        msg = "Spider error processing <%s> (referer: <%s>)" % \
            (request.url, referer)
        log.err(_failure, msg, spider=spider)
        stats.inc_value("spider_exceptions/%s" % _failure.value.__class__.__name__, \
            spider=spider)

    def handle_spider_output(self, result, request, response, spider):
        if not result:
            return defer_succeed(None)
        it = iter_errback(result, self.handle_spider_error, request, spider)
        dfd = parallel(it, self.concurrent_items,
            self._process_spidermw_output, request, response, spider)
        return dfd

    def _process_spidermw_output(self, output, request, response, spider):
        """Process each Request/Item (given in the output parameter) returned
        from the given spider
        """
        if isinstance(output, Request):
            send_catch_log(signal=signals.request_received, request=output, \
                spider=spider)
            self.engine.crawl(request=output, spider=spider)
        elif isinstance(output, BaseItem):
            log.msg(log.formatter.scraped(output, request, response, spider), \
                level=log.DEBUG, spider=spider)
            self.sites[spider].itemproc_size += 1
            dfd = send_catch_log_deferred(signal=signals.item_scraped, \
                item=output, spider=spider, response=response)
            dfd.addBoth(lambda _: self.itemproc.process_item(output, spider))
            dfd.addBoth(self._itemproc_finished, output, spider)
            return dfd
        elif output is None:
            pass
        else:
            log.msg("Spider must return Request, BaseItem or None, got %r in %s" % \
                (type(output).__name__, request), log.ERROR, spider=spider)

    def _check_propagated_failure(self, spider_failure, propagated_failure, request, spider):
        """Log and silence the bugs raised outside of spiders, but still allow
        spiders to be notified about general failures while downloading spider
        generated requests
        """
        # ignored requests are commonly propagated exceptions safes to be silenced
        if isinstance(spider_failure.value, IgnoreRequest):
            return
        elif spider_failure is propagated_failure:
            log.err(spider_failure, 'Unhandled error propagated to spider', \
                spider=spider)
            return # stop propagating this error
        else:
            return spider_failure # exceptions raised in the spider code

    def _itemproc_finished(self, output, item, spider):
        """ItemProcessor finished for the given ``item`` and returned ``output``
        """
        self.sites[spider].itemproc_size -= 1
        if isinstance(output, Failure):
            ex = output.value
            if isinstance(ex, DropItem):
                log.msg(log.formatter.dropped(item, ex, spider), \
                    level=log.WARNING, spider=spider)
                return send_catch_log_deferred(signal=signals.item_dropped, \
                    item=item, spider=spider, exception=output.value)
            else:
                log.err(output, 'Error processing %s' % item, spider=spider)
        else:
            log.msg(log.formatter.passed(output, spider), log.INFO, spider=spider)
            # TODO: remove item_passed 'output' parameter for Scrapy 0.12
            return send_catch_log_deferred(signal=signals.item_passed, \
                item=output, spider=spider, output=output, original_item=item)

