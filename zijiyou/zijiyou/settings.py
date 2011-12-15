# -*- coding: utf-8 -*-
# Scrapy settings for zijiyou project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html

BOT_NAME = 'Mozilla'
BOT_VERSION = '4.0 (compatible; MSIE 6.0; Windows NT 5.1) '
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

SPIDER_MODULES = ['zijiyou.spiders']
NEWSPIDER_MODULE = 'zijiyou.spiders'
DEFAULT_ITEM_CLASS = 'zijiyou.items.zijiyouItem.ResponseBody'
ITEM_PIPELINES=[
                'zijiyou.pipelines.imagesPipeline.ImgPipeline',
                'zijiyou.pipelines.storagePipeline.StoragePipeline' 
                ]

# mongodb setting
DB_HOST = '127.0.0.1' #192.168.0.183 192.168.0.184 127.0.0.1 192.168.0.188
PORT=27017
DB_URL='url'
DB_ITEM='page'
#page按domain分库存储
DB_MAP={
        'page':'page',
        'url':'url',
        'tripfm':'tripfm',
        '17uSpider':'page17u',
        '21cnSpider':'page21cn',
        '55bbsSpider':'page55bbs',
        'bbkerSpider':'pagebbker',
        'bytravelSpider':'pagebytravel',
        'daodaoSpider':'pagedaodao',
        'go2euSpider':'pagego2eu',
        'hexunSpider':'pagehexun',
        'lotourSpider':'pagelotour',
        'lotourbbsSpider':'pagelotourbbs',
        'lvpingSpider':'pagelvping',
        'lvrenSpider':'pagelvren',
        'lvyeSpider':'pagelvye',
        'lvyou114Spider':'pagelvyou114',
        'mafengwoSpider':'pagemafengwo',
        'meishiSpider':'pagemeishi',
        'peopleSpider':'pagepeople',
        'QQBlogSpider':'pageqqblog',
        'sinaSpider':'pagesina',
        'sinabbsSpider':'pagesinabbs',
        'sohuSpider':'pagesohu',
        'sozhenSpider':'pagesozhen',
        'xcarSpider':'pagexcar',
        'yahooSpider':'pageyahoo',
        'baseSeSpider':'pagebasese',
        'bbsSpider2':'pagebbs',
        'jinghuaSpider':'pagejinghua',
        'onegreenSpider':'pageonegreen',
        'daodaoSpider2':'pagedaodao2',
        'baseSeSpider2':'baseSeSpider2',
        }
#url独立数据库存储，按照domain分表存储
DB_URL_COLLECTIONS_MAP = {
                          '17uSpider':'yiqi17u',
                          '21cnSpider':'eryi21cn',
                          '55bbsSpider':'wuwu55bbs',
                          'bbkerSpider':'bbker',
                          'bytravelSpider':'bytravel',
                          'daodaoSpider':'daodao',
                          'go2euSpider':'go2eu',
                          'hexunSpider':'hexun',
                          'lotourSpider':'lotour',
                          'lotourbbsSpider':'lotourbbs',
                          'lvpingSpider':'lvping',
                          'lvrenSpider':'lvren',
                          'lvyeSpider':'lvye',
                          'lvyou114Spider':'lvyou114',
                          'mafengwoSpider':'mafengwo',
                          'meishiSpider':'meishi',
                          'peopleSpider':'people',
                          'QQBlogSpider':'qqblog',
                          'sinaSpider':'sina',
                          'sinabbsSpider':'sinabbs',
                          'sohuSpider':'sohu',
                          'sozhenSpider':'sozhen',
                          'xcarSpider':'xcar',
                          'yahooSpider':'yahoo',
                          'baseSeSpider':'basese',
                          'bbsSpider2':'bbs',
                          'jinghuaSpider':'jinghua',
                          'onegreenSpider':'onegreen',
                          'daodaoSpider2':'daodao2',
                          'baseSeSpider2':'baseSeSpider2',
                          }
DB_ITEM_COLLECTIONS = [
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
                  'KeyList',
                  'ImageItem',#图像
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

LOG_FILE='./zijiyou.log' #./zijiyou.log /home/shiym/spider/zijiyou
LOG_LEVEL='INFO' #INFO DEBUG
DOWNLOAD_DELAY = 8
#遵守robots协议
#ROBOTSTXT_OBEY = True
#爬虫监控器服务的日志
WEBSERVICE_LOGFILE = './webservice.log'
#爬虫监控服务端口
WEBSERVICE_PORT = [6080, 7030]
#多线程
CONCURRENT_REQUESTS_PER_SPIDER= 2
#离线调度阀值 一般设为MAX_INII_REQUESTS_SIZE的80%
PENDING_REQUEST_COUNTER= 80
#pengdingRequest长度限制
MAX_INII_REQUESTS_SIZE = 100
#公网ip更新周期
PROXY_UPDATE_PERIOD = 3600*4 #3600*4
#下载超时
DOWNLOAD_TIMEOUT = 35
#代理公网ip文件
PROXY_FILE_NAME='./proxy.txt'#./proxy.txt /home/shiym/spider/zijiyou
#无效代理的存放路径
PROXY_FILE_NAME_INV = './proxyinv.txt'
#代理无效判断标准
PROXY_DEAD_THRESHOLD = 51
#持续运行爬虫的开关。可以设置为False关掉，当需要测试爬虫的url正则是否能让parser准确地抽取目标url
KEEP_CRAWLING_SWITCH = True
#重复次数
RETRY_TIMES = 5
#重新下载
RETRY_HTTP_CODES = [ '302','400','403','404','407', '408','500','502','503','504']
#遍历方式
#SCHEDULER_ORDER='DFO'
#自动关闭时间：每50分钟
CLOSESPIDER_TIMEOUT = 60 * 50

DIAGNOSER_PATH = './diagnose.log'
OFFLINE_PARSE_LOG = './parselog/'#/home/shiym
#OFFLINE_PARSE_LOG = '/home/cubee/python/spider/spider/zijiyou/offlineParseLog.log'

IMAGES_STORE = './images' #图片存放路径 /home/hy/data/images
IMAGES_EXPIRES = 9999 #到期时间 测试用0，代表每次同一路径图片都会下载，正式运行可以调大无限大，如9999
IMAGES_MIN_HEIGHT = 110
IMAGES_MIN_WIDTH = 110

EXTENSIONS = {
              'zijiyou.extensions.diagnoser.Diagnoser':501
              }

DOWNLOADER_MIDDLEWARES = {
                            'zijiyou.middlewares.downloadermid.RandomHttpProxy': 749,
                            'zijiyou.middlewares.downloadermid.UpdateRequestedUrl':901
                            }

SCHEDULER_MIDDLEWARES = {
                         'zijiyou.middlewares.schedulermid.Cookies': 502
                         }
SPIDER_MIDDLEWARES = {
#                      'zijiyou.middlewares.spidermid.UrlNormalizer': 503, #先归一化再排重
#                      'zijiyou.middlewares.spidermid.DuplicateUrlFilter': 501,
#                      'zijiyou.middlewares.spidermid.UpdateStrategy':500 #进行更新策略，删除PageDb、对应的item的数据库记录
                      #'zijiyou.middlewares.spidermid.SaveNewRequestUrl':499
                      }

##proxy server
#PROXY = ['local']

#Email Configure
MAIL_INTERVAL = 14400
#发送对象列表 
MAIL_TO_LIST = [
                "1413614423@qq.com"
                ]
#设置服务器，用户名、口令以及邮箱的后缀
MAIL = True
MAIL_HOST = 'smtp.sina.com'
MAIL_PORT = 25
MAIL_FROM = 'zijiyou2011@sina.com'
MAIL_USER = 'zijiyou2011'
MAIL_PASS = 'zijiyou'
#MAIL_POSTFIX = 'sina.com'

#检测内存的使用-内存泄漏 scrapy.contrib.memdebug.MemoryDebugger
#MEMDEBUG_ENABLED=True
MEMDEBUG_NOTIFY = [
                "1413614423@qq.com"
                ]
#检测内存的使用-占用内存容量
#MEMUSAGE_ENABLED=True
MEMUSAGE_NOTIFY_MAIL=2000
MEMUSAGE_WARNING_MB=3000
#MEMUSAGE_LIMIT_MB=5048
MEMUSAGE_NOTIFY_MAIL = [
                        "1413614423@qq.com"
                        ]
#telnet setting
TELNETCONSOLE_PORT=[6023, 6073]
TELNETCONSOLE_HOST='0.0.0.0'
TRACK_REFS=True
