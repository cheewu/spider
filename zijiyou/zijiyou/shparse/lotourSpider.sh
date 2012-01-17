#!/bin/sh
cd /home/ubuntu/github/spider/zijiyou #爬虫程序所在路径
date >> ./parselog/lotourSpider		   #记录时间
python parsemain.py lotourSpider >> ./parselog/lotourSpider  #启动执行，输出日志保存在./parselog中
