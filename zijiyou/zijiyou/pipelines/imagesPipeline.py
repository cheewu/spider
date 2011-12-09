#coding: utf-8
'''
Created on 2011-6-22

@author: qingmo
'''
from scrapy import log
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http.request import Request
import datetime

class ImgPipeline(ImagesPipeline):
    '''
    图片管道
    '''
    
    def get_media_requests(self, item, info):
        '''
        下载图片
        '''
        #Article等一个Article包含多个图片
        if item and 'imageUrls' in item:
            self.dtBegin=datetime.datetime.now()
            log.msg("ImagePipeline，开始产生图片请求，并以最高的优先级下载，时间：%s" % datetime.datetime.now(), level=log.INFO)
            for url in item['imageUrls']:
                log.msg("产生一个图片链接请求:%s" % url, level=log.INFO)
                print 'media_requests 图片url：%s'% url        
                yield Request(url)

    def item_completed(self, results, item, info):
        if not (results and len(results)>0) :
            return item
        self.dtEnd=datetime.datetime.now()
        log.msg("图片下载完成，时间花费：%s" % (self.dtEnd - self.dtBegin), level=log.DEBUG)
        print '图片下载完成：结果%s'% results
        item['imagesInfo']=results
        return item
