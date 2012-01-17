#!/bin/sh
cd /home/ubuntu/github/spider/zijiyou #爬虫程序所在路径
date >> ./parselog/bbsSpider2		   #记录时间
python parsemain.py bbsSpider2 >> ./parselog/bbsSpider2  #启动执行，输出日志保存在./parselog中
