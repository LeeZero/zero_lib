#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
from email.header import Header
from email.mime.text import MIMEText
import re
import smtplib

class MailUtil(object):
    @staticmethod
    def sendmail(email, title, message):
        username = 'dev@zmate.cn'
        password = 'Dev2016@zmate'
        smtphost = 'smtp.exmail.qq.com'
        smtpport = 465
        if isinstance(message, unicode):
            message = message.encode('utf-8')
        if isinstance(title, unicode):
            title = title.encode('utf-8')
        msg = MIMEText(message, 'html', 'utf-8')
        msg['Subject'] = Header(title, 'utf-8')
        msg['From'] = username
        if isinstance(email, list):
            msg['To'] = '; '.join(email)
            tolist = email
        else:
            msg['To'] = email
            tolist = [email]
        for i in xrange(0, len(tolist)):
            m = re.search('<([a-z0-9_@\-.]*)>\s*$', tolist[i], re.I)
            if m:
                tolist[i] = m.group(1)
        print "sending mail to", tolist
        #print msg.as_string()
        s = smtplib.SMTP_SSL(smtphost, smtpport)
        s.login(username, password)
        s.sendmail(username, tolist, msg.as_string())
        s.quit()


if __name__ == "__main__":
    if len(sys.argv) == 4 :
        email = sys.argv[1].split(";")
        title = sys.argv[2]
        msg = sys.argv[3]

        MailUtil.sendmail(email, title, msg)