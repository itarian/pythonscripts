# -*- coding: utf-8 -*-

from_mail="abc@gmail.com"  # Provide an email from where it has to send mail
password="********"     # Provide password for the given mail
to_mail="xyz@gmail.com"    # Provide an email where it has to send mail



import os
import subprocess
import ctypes
import re
import sys
import time
import smtplib
import zipfile
import shutil

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

temp=os.environ['PROGRAMDATA']+r'\c1_temp'
temp1=os.environ['PROGRAMDATA']+r'\c2_temp'

if not os.path.exists(temp):
    os.mkdir(temp)

if not os.path.exists(temp1):
    os.mkdir(temp1)

path=r'C:\ProgramData\c1_temp'
dest_path=r'C:\ProgramData\c2_temp'

    
URL= r'http://www.uderzo.it/main_products/space_sniffer/files/spacesniffer_1_3_0_2.zip'
FileName=r'spacesniffer_1_3_0_2.zip'
fb=r'c:\export.csv'
a=r'C:\ProgramData'
print "Deploying "  +FileName+  " begins"

class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)


def Download(path, URL, FileName):
    import urllib2
    import os
    fn = FileName
    fp = os.path.join(path, fn)
    req = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req)
    with open(fp, 'wb') as f:
        while True:
            chunk=con.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    return fp
print "Download Completed"
Download(path, URL, FileName)

def filezip(fp,dest_path):
    fn = FileName
    fp = os.path.join(path, fn)
    with disable_file_system_redirection():
        with zipfile.ZipFile(fp,"r") as zip_ref:
            zip_ref.extractall(dest_path)
            print 'file unzipped to ' +dest_path 
filezip(path,dest_path)

def Execute(dest_path):
    os.chdir(dest_path)
    a=os.popen('SpaceSniffer.exe SpaceSniffer.exe scan c:\ export "Grouped by folder" c:\export.csv autoclose /S').read()
    print 'scanning completed'
    print 'file exported'
    os.chdir(dest_path)
Execute(dest_path)
print 'success'

def file():
    import csv
    with open('c:\export.csv', 'rb') as inf:
        reader = csv.reader(inf)
        with open('c:\export.txt', 'wb') as out:
            writer = csv.writer(out, delimiter='\t')
            writer.writerows(reader)
file()


def mail(from_mail, to_mail, password):
    fromaddr = from_mail
    toaddr = to_mail
     
    msg = MIMEMultipart()
     
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "REPORT OF DRIVE"
     
    body = "Hi,please check the attachment below ,thank you :)"
     
    msg.attach(MIMEText(body, 'plain'))
     
    filename = "export.txt"
    attachment = open("c:\export.txt", "rb")
     
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
    msg.attach(part)
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr,password)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    print 'mail sent successfully to '+toaddr
    server.quit()

mail(from_mail, to_mail, password)
dele=r'C:\export.csv'
dele1=r'C:\export.txt'

try:
    fn = FileName
    fp = os.path.join(path, fn)
    abcdpath=r'C:\ProgramData'
    if os.path.exists(abcdpath):
        os.chdir(os.environ['programdata'])
        shutil.rmtree(temp1)
        shutil.rmtree(temp)
        print 'File removed from your system'
        os.path.exists(os.environ['systemdrive'])
        t1=os.environ['systemdrive']
        path1=t1+'\export.txt'
        os.remove(path1)
        t2=os.environ['systemdrive']
        path2=t2+'\export.csv'
        os.remove(path2)
    else:
        print 'file not removed from your system'
except Exception as err :
    print err
