#!/usr/bin/python3

# utils to send email

import mimetypes
from typing import Any, List
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

# mailConfig is a dict
# mailConfig = {
#     'mail_host': 'smtp.163.com',
#     'mail_user': 'friederich',
#     'mail_pw': 'monster1983',
#     'sender': 'Friederich River<hezhiyuan_tju@163.com>
# }

mail_config = {
    'mail_host': 'smtp.163.com',
    'mail_user': 'friederich',
    'mail_pw': 'monster1983',
    'sender': 'Friederich River<hezhiyuan_tju@163.com>'
}


# mailObject is a class

class MailObject(object):
    # input parameters contains:
    # mailReciever, mailSubject, mailContent, Attachment
    def __init__(self, mail_reciever, mail_subject, mail_content, attachment, charset='utf-8'):
        self.charset = charset
        # if attachment is None content_type is text/plain else content_type is multipart/mixed
        if attachment:
            self.mail_content = MIMEMultipart('mixed')
            self.set_content(self.mail_content)
            self.set_attachment(attachment)
        else:
            self.mail_content = MIMEText(mail_content, 'plain', 'utf-8')
            self.set_content(mail_content)
        self.set_reciever(mail_reciever)
        self.set_subject(mail_subject)
        
        
    
    # set mail reciever
    def set_reciever(self, mail_reciever: List[str]):
        self.mail_content['To'] = ','.join(mail_reciever)
    
    # set mail title
    def set_subject(self, mail_subject):
        self.mail_content['Subject'] = Header(mail_subject, 'utf-8')
    
    # set mail content
    def set_content(self, mail_content):
        self.mail_content = mail_content
    
    # set mail attachment
    def set_attachment(self, attachment):
        if isinstance(attachment, MIMEText):
            self.mail_content.attach(attachment)
        elif isinstance(attachment, list):
            for att in attachment:
                self.mail_content.attach(att)
        else:
            self.mail_content.attach(attachment)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.mail_content


# function auto_content_type
# auto detect the content type of a file
# file_name is a string input
# return a string of content type
def auto_content_type(file_name):
    return mimetypes.guess_type(file_name)[0] or 'text/plain'

# AttachmentBase is a class
# defines the attachment of a mail

class AttachmentBase(object):
    # input parameters contains:
    # attachmentName, attachmentPath
    def __init__(self, attachment_name, attachment_path):
        self.attachment_name = attachment_name
        self.attachment_path = attachment_path
        self.attachment = MIMEText(open(self.attachment_path, 'rb').read(), 'base64', 'utf-8')
        self.attachment['Content-Type'] = auto_content_type(self.attachment_path)
        self.attachment['Content-Disposition'] = 'attachment; filename=f"{self.attachment_name}"'

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.attachment



# mailServer is a class
# recieve a mailConfig dict

import smtplib

class MailServer(object):
    # init basic infomation of mail sender
    def __init__(self, mail_config):
        self.__mail_host = mail_config['mail_host']
        self.__mail_user = mail_config['mail_user']
        self.__mail_pw = mail_config['mail_pw']
        self.sender = mail_config['sender']
        self.mail_server = smtplib.SMTP()

    # provide a smtp config
    def smtp_config(self):
        try:
            self.mail_server = smtplib.SMTP()
            self.mail_server.connect(self.__mail_host, 25)
            self.mail_server.login(self.__mail_user, self.__mail_pw)
        except smtplib.SMTPException:
            raise smtplib.SMTPException
    
    # provide a smtp ssl config
    def smtp_ssl_config(self):
        try:
            self.mail_server = smtplib.SMTP_SSL(self.__mail_host, 465)
            self.mail_server.login(self.__mail_user, self.__mail_pw)
        except smtplib.SMTPException:
            raise smtplib.SMTPException
        
    # shutdown the smtp server
    def shutdown(self):
        self.mail_server.quit()

    # send mail
    def send_mail(self, mail):
        try:
            self.mail_server.sendmail(
                self.sender, mail['To'].split(','),
                mail.as_string())
        except smtplib.SMTPException:
            raise smtplib.SMTPException

    