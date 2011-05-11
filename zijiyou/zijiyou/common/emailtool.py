# -*- coding: utf-8 -*-
'''
Created on 2011-5-11

@author: hy
'''
#!/usr/bin/env python
# -*- coding: gbk -*-
#导入smtplib和MIMEText
from email.mime.text import MIMEText
from scrapy import log, spider
from scrapy.conf import settings
import smtplib
import datetime

def sendMail(sub,content):
    '''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("sub","content")
    '''
    mailHost = settings.get('MAIL_HOST', None)
    mailUser = settings.get('MAIL_USER', None)
    mailPass = settings.get('MAIL_PASS', None)
    mail_postfix = settings.get('MAIL_POSTFIX', None)
    toList = settings.get('MAIL_TO_LIST', None)
    
    if not (mailHost and mailUser and mailPass and mail_postfix and toList):
        log.msg("发送邮件前，请在settings配置email信息", level=log.ERROR)
        return
    
    
    me=mailUser+"<"+mailUser+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(toList)
    try:
        s = smtplib.SMTP()
        s.connect(mailHost)
        s.login(mailUser,mailPass)
        s.sendmail(me, toList, msg.as_string())
        s.close()
        log.msg("邮件发送成功 %s" % datetime.datetime.now(), level=log.INFO)
        return True
    except Exception, e:
        log.msg("邮件发送失败，%s" % str(e) , level=log.ERROR)
        log.msg("请检测settings中的email配置信息", level=log.ERROR)
        #print str(e)
        return False
