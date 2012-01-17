#!/bin/sh
cd /home/ubuntu/github/spider/zijiyou #爬虫程序所在路径
date >> ./parselog/17uSpider		   #记录时间
python parsemain.py 17uSpider >> ./parselog/17uSpider  #启动执行，输出日志保存在./parselog中
