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
DB_COLLECTIONS = ['daodaoCol', 'responseCol']

LOG_FILE='./zijiyou.log'
CONCURRENT_REQUESTS_PER_SPIDER=1
DOWNLOAD_DELAY = 10

