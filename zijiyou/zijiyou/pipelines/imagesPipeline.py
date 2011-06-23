#coding: utf-8
'''
Created on 2011-6-22

@author: qingmo
'''
from scrapy import log
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http.request import Request
import datetime

class ImagesPipeline(ImagesPipeline):
    '''
    图片管道
    '''
    
    def get_media_requests(self, item, info):
        if item and 'imageUrls' in item:
            self.dtBegin=datetime.datetime.now()
            print '测试 imgpipeline 发出图片下载请求%s' % item['imageUrls']
            log.msg("ImagePipeline，开始产生图片请求，并以最高的优先级下载，时间：%s" % datetime.datetime.now(), level=log.INFO)
            for url in item['imageUrls']:
                log.msg("产生一个图片链接请求:%s" % url, level=log.INFO)
                print '测试 图片url：%s'% url        
                yield Request(url)

    def item_completed(self, results, item, info):
        if not (results and len(results)>1) :
            print '测试 到达imgpipeline 但没有图片%s' % item
            return item
        self.dtEnd=datetime.datetime.now()
        log.msg("图片下载完成，时间花费：%s" % (self.dtEnd - self.dtBegin), level=log.INFO)
        print '测试 下载完成：结果%s'% results
        item['imagesInfo']=results
        return item
