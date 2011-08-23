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
ITEM_PIPELINES=[
#                'zijiyou.pipelines.imagesPipeline.ImagesPipeline',
                'zijiyou.pipelines.storagePipeline.StoragePipeline' 
                ]

# mongodb setting
DB_HOST = '127.0.0.1' #192.168.0.183 192.168.0.185 127.0.0.1 192.168.0.188
DB_PORT=27017
DB='sespider'#spiderV21 spidertest bbstest
DB_COLLECTIONS = ['PageDb',
                  'UrlDb',
                  'POI',
                  'Attraction',
                  'Hotel',
                  'Region',
                  'Article',
                  'Article1',
                  'Article2',
                  'Article3',
                  'Article4',
                  'BBSArticle',
                  'Note',
                  'MemberInfo',
                  'MemberTrack',
                  'MemberFriend',
                  'MemberNoteList',
                  'KeyWord',
                  'ImageDb',
                  'Profile',
                  'KeyList'
                  ]
COLLECTION_NAME_MAP = {
                    'Attraction':'POI',
                    'article':'POI',
                    'note':'Note',
                    'Hotel':'POI',
                    'Article1':'Article',
                    'Article2':'Article',
                    'Article3':'Article',
                    'Article4':'Article',
                    'BBSArticle':'Article',
}
BBS_SPIDER_NAME = [
        '55bbsSpider',
        'go2euSpider',
        'xcarSpider',
        'sinabbsSpider',
        'lvyeSpider',
        'lotourbbsSpider',
]

CRAWL_DB = 'UrlDb'
RESPONSE_DB = 'PageDb'
LOG_FILE='./zijiyou.log'
LOG_LEVEL='INFO' #INFO DEBUG
DOWNLOAD_DELAY = 0.5
CONCURRENT_REQUESTS_PER_SPIDER=6
RECENT_URLS_SIZE = 3000000
MAX_INII_REQUESTS_SIZE = 1000000
#CLOSESPIDER_TIMEOUT=1800
#CLOSESPIDER_ITEMPASSED=3000
SCHEDULER_ORDER='DFO'

DIAGNOSER_PATH = './diagnose.log'
OFFLINE_PARSE_LOG = './offlineParseLog.log'#/home/shiym
#OFFLINE_PARSE_LOG = '/home/cubee/python/spider/spider/zijiyou/offlineParseLog.log'

IMAGES_STORE = '/data/images' #图片存放路径 /home/hy/data/images
IMAGES_EXPIRES = 9999 #到期时间 测试用0，代表每次同一路径图片都会下载，正式运行可以调大无限大，如9999
IMAGES_MIN_HEIGHT = 110
IMAGES_MIN_WIDTH = 110

EXTENSIONS = {'zijiyou.extensions.diagnoser.Diagnoser':501
              }

DOWNLOADER_MIDDLEWARES = {
#                            'zijiyou.middlewares.downloadermid.RandomHttpProxy': 750,
                            'zijiyou.middlewares.downloadermid.UpdateRequestedUrl':901
                            }

SCHEDULER_MIDDLEWARES = {'zijiyou.middlewares.schedulermid.Cookies': 502}
SPIDER_MIDDLEWARES = {
#                      'zijiyou.middlewares.spidermid.UrlNormalizer': 503, #先归一化再排重
#                      'zijiyou.middlewares.spidermid.DuplicateUrlFilter': 501,
#                      'zijiyou.middlewares.spidermid.UpdateStrategy':500 #进行更新策略，删除PageDb、对应的item的数据库记录
                      #'zijiyou.middlewares.spidermid.SaveNewRequestUrl':499
                      }

#proxy server
PROXY = ['local']

#Email Configure
MAIL_INTERVAL = 14400
#发送对象列表 
MAIL_TO_LIST = [
                "953227024@qq.com", 
                "1413614423@qq.com"
                ]
#设置服务器，用户名、口令以及邮箱的后缀
MAIL= True
MAIL_HOST = 'smtp.sina.com'
MAIL_PORT = 25
MAIL_FROM = 'zijiyou2011@sina.com'
MAIL_USER = 'zijiyou2011'
MAIL_PASS = 'zijiyou'
#MAIL_POSTFIX = 'sina.com'

#检测内存的使用-内存泄漏 scrapy.contrib.memdebug.MemoryDebugger
#MEMDEBUG_ENABLED=True
MEMDEBUG_NOTIFY = [
                "953227024@qq.com", 
                "1413614423@qq.com"
                ]
#检测内存的使用-占用内存容量
#MEMUSAGE_ENABLED=True
MEMUSAGE_NOTIFY_MAIL=2000
MEMUSAGE_WARNING_MB=3000
#MEMUSAGE_LIMIT_MB=5048
MEMUSAGE_NOTIFY_MAIL = [
                        "953227024@qq.com", 
                        "1413614423@qq.com"
                        ]


#URLNormallizer_Rules(URL 归一化)
#URLNORMALIZER_RULES = {
#                       r'(\?|\&amp;|\&amp;amp;)PHPSESSID=[a-zA-Z0-9]{32}$':r'',
#                       r'(\?|&)PHPSESSID=[a-zA-Z0-9]{32}(&?)(.*)':r'\1\3'
#                       }

#telnet setting
TELNETCONSOLE_PORT=[6023, 6073]
TELNETCONSOLE_HOST='0.0.0.0'
TRACK_REFS=True