# -*- coding: utf-8 -*-
'''
Created on 2011-4-12

@author: shiym
'''
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from scrapy.utils.httpobj import urlparse_cached
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from twisted.internet import reactor
from urllib import unquote, proxy_bypass
from urllib2 import _parse_proxy
from urlparse import urlunparse
from zijiyou.db.middlewaresApt import DownloaderApt
import base64
import datetime

class ErrorFlag(object):
    ACCESS_DENY_FLAG = 0
    
class UpdateRequestedUrl(object):
    '''
    访问过的url更新数据库
    '''
    def __init__(self):
        self.apt=DownloaderApt()
    
    def process_response(self, request, response, spider):
        responseStatus=response.status
        if responseStatus in [400, 403, 304,404]:
            log.msg("%s 错误！url:%s" % (responseStatus,request.url), level=log.ERROR)
        if 'urlId' in request.meta:
            urlId=request.meta['urlId']
            self.apt.updateUrlDbStatusById(urlId,spider.name, status=responseStatus)
            log.msg("用urlId更新url访问状态 url:%s" % request.url, level=log.INFO)
        else:
#            self.apt.updateUrlDbStatusByUrl(request.url,spider.name, status=responseStatus)
            log.msg("没有urlId，请确认是否种子url url:%s" % request.url, level=log.WARNING)
        return response

class RandomHttpProxy(object):
    def __init__(self):
        self.proxies = {}
        
        #数据库适配器
        self.apt=DownloaderApt()
        #循环代理计数器
        self.proxyCounter=0
        #公网ip更新周期
        self.proxyUpdatePeriod=settings.get('PROXY_UPDATE_PERIOD')
        #代理公网ip文件
        self.proxyFile=settings.get('PROXY_FILE_NAME')
        #无效代理的存放路径
        self.proxyFileInv = settings.get('PROXY_FILE_NAME_INV')
        #初始化代理
        self.proxyDeadThreshold=settings.get('PROXY_DEAD_THRESHOLD')
        #无效代理缓存表
        self.proxyDead=set()
        #当前收集的无效代理
        self.proxyInv = set()
        #在爬虫结束前保存无效代理
        dispatcher.connect(self.saveInvProxy, signal = signals.spider_closed)
        self.updateProxy()

        if not self.proxies:
            raise NotConfigured

    def saveInvProxy(self,spider=None):
        '''
        保存当前收集到的无效代理列表到无效代理文件中
        '''
        finv1 = open(self.proxyFileInv,'a')
        for p in self.proxyInv:
            finv1.write('\n')
            finv1.write(p)
        finv1.close()

    def updateProxy(self):
        """
        加载代理列表，更新代理
        """
        print '加载或更新公网代理：%s' % datetime.datetime.now()
        log.msg('加载或更新公网代理：%s' % datetime.datetime.now(),level=log.INFO)
        counter = 0
        self.saveInvProxy()
        #更新无效代理过滤表
        finv2 = open(self.proxyFileInv)
        for p in finv2:
            if len(p) > 10:
                self.proxyDead.add(p.strip())
        finv2.close()
        #加载代理
        f=open(self.proxyFile)
        for p in f:
            pdict=p.split('=')
            if len(pdict) == 2 and len(pdict[0])>2 and len(pdict[1]) > 5:
                type=pdict[0].strip()
                url=pdict[1].strip()
                if not type in self.proxies.keys():
                    self.proxies[type]=[]
                creds, proxyUrl=self._get_proxy(url, type)
                #过滤无效代理
                if proxyUrl in self.proxyDead:
                    continue
                newProxy={'creds':creds,'proxyUrl':proxyUrl,'failsNum':0}
                #本机代理永不失效
                if url[:9] == '127.0.0.1':
                    newProxy['failNum'] = -999999999
                self.proxies[type].append(newProxy)
                counter += 1
            else:
                print '无效的代理：%s' % p
                log.msg('无效的代理：%s' % p,level=log.ERROR)
        print '加载或更新公网代理数:%s' % counter
        #周期性加载更新
        reactor.callLater(self.proxyUpdatePeriod, self.updateProxy)
        f.close()

#    def clearProxyDead(self):
#        """
#        清空无效proxy缓存表
#        """
#        print '清空无效proxy缓存表：%s' % datetime.datetime.now()
#        log.msg('清空无效proxy缓存表：%s' % datetime.datetime.now(),level=log.INFO)
#        self.proxyDead = []
#        reactor.callLater(self.proxyUpdatePeriod*10,self.clearProxyDead)

    def _get_proxy(self, url, orig_type):
        proxy_type, user, password, hostport = _parse_proxy(url)
        proxy_url = urlunparse((proxy_type or orig_type, hostport, '', '', '', ''))

        if user and password:
            user_pass = '%s:%s' % (unquote(user), unquote(password))
            creds = base64.b64encode(user_pass).strip()
        else:
            creds = None

        return creds, proxy_url

    def process_request(self, request, spider):
        # ignore if proxy is already seted
        if 'proxy' in request.meta:
            return

        parsed = urlparse_cached(request)
        scheme = parsed.scheme

        # 'no_proxy' is only supported by http schemes
        if scheme in ('http', 'https') and proxy_bypass(parsed.hostname):
            return

        if scheme in self.proxies:
            self._set_proxy(request, scheme)
    
    def process_response(self,request,response,spider):
        """
        如果下载失败，可能是代理有失效。
        需要更新代理失败次数以便标识出无效的代理；更新次request的代理，交给引擎判定是否需要再次发送该请求
        """
        cstatus=response.status
        #处理下载失败：更新下载失败次数、清除无效代理
        if cstatus > 302:
            parsed = urlparse_cached(request)
            scheme = parsed.scheme
            if scheme in self.proxies and 'proxy' in request.meta:
                proxy=request.meta['proxy']
                #更新代理的失败次数
                for pdict in self.proxies[scheme]:
                    if proxy == pdict['proxyUrl']:
                        #判断代理的失败次数是否超出限定
                        if pdict['failsNum'] >= self.proxyDeadThreshold:
                            self.proxies[scheme].remove(pdict)
                            self.proxyInv.add(proxy)
                        else:
                            pdict['failsNum'] = 1+pdict['failsNum']
                        break
                #更新次request的代理
                self._set_proxy(request, scheme)
        
        return response
    
    def process_exception(self,request,exception,spider):
        """
        下载异常，可能是代理无效了，对代理进行惩罚性失败次数更新：10
        """
        print '下载异常，可能是被封锁了ip或代理无效，异常：%s 代理：%s url:%s' % (exception,('proxy' in request.meta and request.meta['proxy'] or '无'),request.url)
        log.msg('下载异常，可能是被封锁了ip或代理无效，异常：%s 代理：%s url:%s' % (exception,('proxy' in request.meta and request.meta['proxy'] or '无'),request.url), level=log.WARNING)
        parsed = urlparse_cached(request)
        scheme = parsed.scheme
        if scheme in self.proxies and 'proxy' in request.meta:
            proxy=request.meta['proxy']
            #更新代理的失败次数
            for pdict in self.proxies[scheme]:
                if proxy == pdict['proxyUrl']:
                    #判断代理的失败次数是否超出限定
                    if pdict['failsNum'] >= self.proxyDeadThreshold:
                        self.proxies[scheme].remove(pdict)
                        self.proxyInv.add(proxy)
                    else:
                        pdict['failsNum'] = 20+pdict['failsNum']
                    break
        #更新代理
        self._set_proxy(request, scheme)
        #更新数据库的url状态为800
        if 'urlId' in request.meta:
            urlId=request.meta['urlId']
            self.apt.updateUrlDbStatusById(urlId,spider.name, status=800)
            log.msg("用urlId更新url访问状态为异常 url:%s" % request.url, level=log.INFO)
            print "用urlId更新url访问状态为异常 url:%s" % request.url
        return None
    
    def _set_proxy(self, request, scheme):
        """
        循环选择一个代理ip
        """
        proxyOrg = 'proxy' in request.meta and request.meta['proxy'] or '无'
        proxyLength = len(self.proxies[scheme])
        if proxyLength == 0:
            #取消代理，直接访问
            if 'proxy' in request.meta:
                request.meta.pop('proxy')
#            print '代理列表为空！ 当前request的代理：%s' %('proxy' in request.meta and request.meta['proxy'] or '无')
        else:
            self.proxyCounter +=1
            proxyIndex = self.proxyCounter % proxyLength
            proxydict = self.proxies[scheme][proxyIndex]
            creds=proxydict['creds']
            proxy=proxydict['proxyUrl']
            proxyNew = proxy
            
            request.meta['proxy'] = proxy
            if creds:
                request.headers['Proxy-Authorization'] = 'Basic ' + creds
            print '更新代理。原代理：%s  新代理：%s' % (proxyOrg,proxyNew)
            
            