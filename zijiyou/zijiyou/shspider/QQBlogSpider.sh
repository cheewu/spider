#!/bin/sh
cd /home/ubuntu/github/spider/zijiyou #爬虫程序所在路径
date >> ./parselog/QQBlogSpider		   #记录时间
python spidermain.py QQBlogSpider >> ./parselog/QQBlogSpider  #启动执行，输出日志保存在./parselog中
