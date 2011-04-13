# -*- coding: utf-8 -*-
# Scrapy settings for zijiyou project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html

BOT_NAME = 'zijiyou'
BOT_VERSION = '1.0'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

SPIDER_MODULES = ['zijiyou.spiders']
NEWSPIDER_MODULE = 'zijiyou.spiders'
DEFAULT_ITEM_CLASS = 'zijiyou.items.zijiyouItem.ZijiyouItem'
ITEM_PIPELINES=['zijiyou.pipelines.pipelines.ZijiyouPipeline']

# mongodb setting
DB_HOST = 'localhost'
DB_PORT=27017
DB='daodaoDb'
DB_COLLECTIONS = ['daodaoCol', 'responseCol', 'noteCol']

LOG_FILE='./zijiyou.log'
#CONCURRENT_REQUESTS_PER_SPIDER=1
DOWNLOAD_DELAY = 2

DOWNLOADER_MIDDLEWARES = {'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
                          'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
                            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
                            'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
                            'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
                            'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
                            'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
                            'zijiyou.middlewares.downloadermid.RandomHttpProxy': 750,
                            'zijiyou.middlewares.downloadermid.ResponseStatusCheck': 770,
                            'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 800,
                            'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
                            'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900
                            }

#proxy server
#PROXY = ['http://127.0.0.1:8081', 'http://113.105.168.172:8080', 'http://124.248.34.51:3128', 'local']
#PROXY = ['http://127.0.0.1:8081', 'http://113.105.168.172:8080', 'http://124.248.34.51:3128', 'local']
