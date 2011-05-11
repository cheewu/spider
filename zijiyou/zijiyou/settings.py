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
                  'KeyWord',
                  'CityAttraction',
                  'test']

LOG_FILE='./zijiyou.log'
#TESTLOG='/data/configs/test.txt'
LOG_LEVEL='INFO'
DOWNLOAD_DELAY = 0.2
CONCURRENT_REQUESTS_PER_SPIDER=1
RECENT_URLS_SIZE = 3000
MAX_INII_REQUESTS_SIZE = 1000
#CLOSESPIDER_TIMEOUT=1800
#CLOSESPIDER_ITEMPASSED=3000
SCHEDULER_ORDER='DFO'

DIAGNOSER_PATH = '/data/configs/diagnose.log'
OFFLINE_PARSE_LOG = '/data/configs/offlineParseLog.log'#/home/shiym

EXTENSIONS = {'zijiyou.extensions.diagnoser.Diagnoser':501
              }

DOWNLOADER_MIDDLEWARES = {
#                            'zijiyou.middlewares.downloadermid.RandomHttpProxy': 750,
                            'zijiyou.middlewares.downloadermid.UpdateRequestedUrl':901
                            }

#SCHEDULER_MIDDLEWARES = {'zijiyou.middlewares.schedulermid.RequestSaver': 502}
SPIDER_MIDDLEWARES = {
                      'zijiyou.middlewares.spidermid.DuplicateUrlFilter': 501,
                      #'zijiyou.middlewares.spidermid.SaveNewRequestUrl':499
                      }

#proxy server
PROXY = ['local']
