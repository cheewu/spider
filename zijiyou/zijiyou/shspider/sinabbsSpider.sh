#!/bin/sh
cd /home/ubuntu/github/spider/zijiyou #爬虫程序所在路径
date >> ./parselog/sinabbsSpider		   #记录时间
python spidermain.py sinabbsSpider >> ./parselog/sinabbsSpider  #启动执行，输出日志保存在./parselog中
