#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from tools import ReadConfig

class Smtp:
    def __init__(self,):
        self.configdata = ReadConfig.ReadConfig()
        self.msg = email.mime.multipart.MIMEMultipart()
        self.msg['from'] = self.configdata.get_data('EAMAIL','email_sendaddr')
        self.msg['to'] = self.configdata.get_data('EAMAIL','email_recipientaddrs')
        self.msg['subject'] = self.configdata.get_data('EAMAIL','email_subject')
        content = self.configdata.get_data('EAMAIL','email_content')
        txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
        self.msg.attach(txt)
        

    def add_accessory(self,accessoryfile):
        part = MIMEApplication(open(accessoryfile,'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=accessoryfile.split('\\')[-1])#参数为路径，文件名截取路径\后字段
        self.msg.attach(part)

    def send_email(self,):
        smtpHost = self.configdata.get_data('EAMAIL','email_smtphost')
        password = self.configdata.get_data('EAMAIL','email_password')
        smtp = smtplib.SMTP()
        smtp.connect(smtpHost, '25')
        smtp.login(self.msg['from'], password)
        try:
            smtp.sendmail(self.msg['from'], self.msg['to'], str(self.msg))
            print("邮件发送成功！")
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)
        finally:
            smtp.quit()


        
        
        
      