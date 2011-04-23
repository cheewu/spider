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
DEFAULT_ITEM_CLASS = 'zijiyou.items.zijiyouItem.ResponseBody'
ITEM_PIPELINES=['zijiyou.pipelines.pipelines.ZijiyouPipeline']

# mongodb setting
DB_HOST = 'localhost'
DB_PORT=27017
DB='spiderV20'
DB_COLLECTIONS = ['ResponseBody',
                  'Attraction',
                  'Note',
                  'CrawlUrl',
                  'CommonSense',
                  'MemberInfo',
                  'MemberTrack',
                  'MemberFriend',
                  'MemberNoteList',
                  'test']

LOG_FILE='./zijiyou.log'
DOWNLOAD_DELAY = 1.2
CONCURRENT_REQUESTS_PER_SPIDER=1
RECENT_URLS_SIZE = 3000
MAX_INII_REQUESTS_SIZE = 1000
CLOSESPIDER_TIMEOUT=1800
CLOSESPIDER_ITEMPASSED=3000
SCHEDULER_ORDER='DFO'

DOWNLOADER_MIDDLEWARES = {
                            'zijiyou.middlewares.downloadermid.RandomHttpProxy': 750,
                            'zijiyou.middlewares.downloadermid.RequestedUrlSaveAndUpdate':901
                            }

#SCHEDULER_MIDDLEWARES = {'zijiyou.middlewares.schedulermid.RequestSaver': 502}
SPIDER_MIDDLEWARES = {'zijiyou.middlewares.spidermid.DuplicateUrlFilter': 501}

#proxy server
PROXY = ['http://127.0.0.1:8081', 
         'http://125.210.188.36:80',
         'http://221.179.35.89:80',
         'http://211.139.10.173:80',
         'http://60.28.212.184:80',
         'http://202.171.253.70:80',
         'http://211.139.195.23:80',
         'http://218.195.101.80:3128',
         'http://221.204.246.161:8001',
         'http://218.207.217.226:80',
         'http://218.207.217.227:80',
         'http://123.125.156.92:80',
         'http://221.204.246.21:8080',
         'http://114.255.171.231:80',
         'http://211.139.10.182:80',
         'http://124.248.34.50:3128',
         'http://124.248.34.51:3128',
         'http://221.204.246.161:80',
         'http://211.139.10.183:80',
         'http://218.14.227.197:3128',
         'local']
