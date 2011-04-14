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
DB_COLLECTIONS = ['daodaoCol', 
                  'responseCol',
                  'crawlCol',
                  'noteCol']

LOG_FILE='./zijiyou.log'
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_SPIDER=1
RECENT_URLS_SIZE = 3000
CLOSESPIDER_TIMEOUT=3600
CLOSESPIDER_ITEMPASSED=1000

DOWNLOADER_MIDDLEWARES = {
#                          'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
#                          'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
#                            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
#                            'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
#                            'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
#                            'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
#                            'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
                            'zijiyou.middlewares.downloadermid.RandomHttpProxy': 750,
                            'zijiyou.middlewares.downloadermid.ResponseStatusCheck': 770,
#                            'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 800,
#                            'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
#                            'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900
                            'zijiyou.middlewares.downloadermid.RequestedUrlUpdate':901
                            }

SCHEDULER_MIDDLEWARES = {'zijiyou.middlewares.schedulermid.RequestSaver': 501}

#proxy server
PROXY = ['http://127.0.0.1:8081', 
         'http://222.216.108.167:8081', 
         'http://117.34.73.50:80', 
         'http://111.1.32.121:80', 
         'http://222.86.192.246:3128',
         'http://124.248.34.51:3128', 
         'http://222.173.162.21:563', 
         'local']
