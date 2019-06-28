path=r'C:\Program Files\Internet Explorer'  #Provide your file/folder path
days=10      #Provide your preferred days limitation

emailto=['tamil@yopmail.com']  # Provide an "To email address" where the report would be sent.You can also provide multiple To email address For example: ['tamil@yopmail.com','sensor@yopmail.com']
emailfrom='patchreport1@gmail.com'  #Provide "from Email address"
password='Patchreport@123'          #Provide "from Email address's" Password
smtpserver='smtp.gmail.com'
port=587

msgbody=r'''Hi

Please find the endpoint's folder/file creation/modification report file in the attachment for your reference.

Thank you.'''

import os
import datetime
import math
import ctypes
import time
import re
import sys
import shutil
import random
import socket
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

le_path=os.environ['TEMP']
file_path=os.path.join(le_path,r'report.txt')
ale=0


def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))


def computername():
    return os.environ['COMPUTERNAME']

def ipaddress():
    return socket.gethostbyname(socket.gethostname())

def emailreport(subject, emailto,emailfrom,file_path,password,smtpserver,port,msgbody):
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ",".join(emailto)
    msg["Subject"] = subject
    msg.preamble = subject
    body = MIMEText(msgbody)
    msg.attach(body)       
    with open(file_path, 'rb') as fp:
        record = MIMEBase('text', 'octet-stream')
        record.set_payload(fp.read())
        encoders.encode_base64(record)
        record.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        msg.attach(record)
    try:
        server = smtplib.SMTP(smtpserver,port)
        server.ehlo()
        server.starttls()
        server.login(emailfrom, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        return " \nThe email report has been sent to "+msg["To"]
    except Exception as e:
        return e

def file_edit(dir_path,fi_time):
    try:
        with open(file_path, 'a') as fi:
            fi.write("\n")
            fi.write(dir_path)
            fi.write('        ')
            fi.write(fi_time)
            fi.write("\n")
    except:
        print 'ERROR- Report Generation failed!!!'

try:
    with open(file_path, 'a') as fi:
        fi.writelines('Folders/files are created newly from your file path:(In last %d days)' % (days))
        fi.write("\n")
        fi.writelines('----------------------------------------------------')             
        fi.write("\n")
except:
    print 'ERROR- Report Generation failed!!!'

import os, time
now = time.time()
try:
    for root, directories, filenames in os.walk(path):
        for directory in directories:
            dir_path=os.path.join(root, directory)
            diff=now - os.stat(dir_path).st_ctime
            if diff < (days * 86400):
                fi_time=time.ctime(os.stat(dir_path).st_ctime)
                file_edit(dir_path,fi_time)
                ale=ale+1
        for filename in filenames: 
            dir_path=os.path.join(root,filename)
            diff=now - os.stat(dir_path).st_ctime
            if diff < (days * 86400):
                fi_time=time.ctime(os.stat(dir_path).st_ctime)       
                file_edit(dir_path,fi_time)
                ale=ale+1
except Exception as err: 
    print "Failed due to the below error"
    print err
    
try:
    with open(file_path, 'a') as fi:
        for i in range(0,4):
            fi.write("\n")
        fi.writelines('Folders/files are modified from your file path:(In last %d days)' % (days))
        fi.write("\n")
        fi.writelines('------------------------------------------------')             
        fi.write("\n")
except:
    print 'ERROR- Report Generation failed!!!'


import os, time
now = time.time()
try:
    for root, directories, filenames in os.walk(path):
        for directory in directories:
            dir_path=os.path.join(root, directory)
            diff=now - os.stat(dir_path).st_mtime
            if diff < (days * 86400):
                fi_time=time.ctime(os.stat(dir_path).st_mtime)
                file_edit(dir_path,fi_time)
                ale=ale+1
        for filename in filenames: 
            dir_path=os.path.join(root,filename)
            diff=now - os.stat(dir_path).st_mtime
            if diff < (days * 86400):
                fi_time=time.ctime(os.stat(dir_path).st_mtime)
                file_edit(dir_path,fi_time)
                ale=ale+1
except Exception as err: 
    print "Failed due to the below error"
    print err

subject='%s %s File modified report'%(computername(), ipaddress())

if ale==0:
    print 'No modifications are made in your file path (%s)' % (path)
    alert(0)
else:
    print 'Some Folders/files/subfolders modifications are made in your file path (%s)' % (path)
    emailreport(subject, emailto,emailfrom,file_path,password,smtpserver,port,msgbody)
    print "Mail has been sent to %s !!!!" % (emailto)
    alert(1)

if os.path.exists(file_path):
    os.remove(file_path)
