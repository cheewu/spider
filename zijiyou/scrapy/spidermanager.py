"""
SpiderManager is the class which locates and manages all website-specific
spiders
"""

from zope.interface import implements

from scrapy import log, signals
from scrapy.interfaces import ISpiderManager
from scrapy.utils.misc import walk_modules
from scrapy.utils.spider import iter_spider_classes
from scrapy.xlib.pydispatch import dispatcher


class SpiderManager(object):

    implements(ISpiderManager)

    def __init__(self, spider_modules):
        self.spider_modules = spider_modules
        self._spiders = {}
        for name in self.spider_modules:
            for module in walk_modules(name):
                self._load_spiders(module)
        dispatcher.connect(self.close_spider, signals.spider_closed)

    def _load_spiders(self, module):
        for spcls in iter_spider_classes(module):
            self._spiders[spcls.name] = spcls

    @classmethod
    def from_settings(cls, settings):
        return cls(settings.getlist('SPIDER_MODULES'))

    def create(self, spider_name, **spider_kwargs):
        return self._spiders[spider_name](**spider_kwargs)

    def find_by_request(self, request):
        return [name for name, cls in self._spiders.iteritems()
            if cls.handles_request(request)]

    def list(self):
        return self._spiders.keys()

    def close_spider(self, spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)
