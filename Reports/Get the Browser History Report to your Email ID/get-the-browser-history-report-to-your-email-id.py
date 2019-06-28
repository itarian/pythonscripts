FromDate='08-02-2018' ## Mention the date range to start
ToDate='19-06-2018' ## Mention the date range to stop
emailto='xxxxxx@yyyyy.com' # To address
import xml.etree.ElementTree as ET
import getpass
import socket
import _winreg
import os
import subprocess
import ctypes
import re
import sys
import time
import smtplib
import zipfile
import shutil
import random
import urllib2
def computername():
    import os
    return os.environ['COMPUTERNAME']

## get ip address
def ipaddress():
    import socket
    return socket.gethostbyname(socket.gethostname())
def Email(fileToSend,To):
    from mailjet_rest import Client
    import os
    api_key='3e70858a7a5c5fbc245a662d5d9aa238'   # API KEY of Mail Jet 
    api_secret= 'a337abcc84d8fb062f6f1597d966ae6f'  # API SECRET KEY of Mail Jet
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    import base64
    with open(fileToSend, 'rb') as fp:
        ki=base64.b64encode(fp.read())
    data = {
      'Messages': [
                    {
                            "From": {
                                    "Email": "c1operations123@gmail.com",
                            },
                            "To": [
                                    {
                                            "Email": "%s"%To,
                                    }
                            ],
                            "Subject": "Browsing history ",
                            "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
                            "HTMLPart": """<h3> Hi

        Please find the attachment which contains all the device reports 

        Thank you.</h3>""",
                            "Attachments": [
                                    {
                                            "ContentType": "text/csv",
                                            "Filename": "Finalreport.csv",
                                            "Base64Content": "%s"%ki
                                    }
                            ]
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    ret=result.status_code
    if ret==200:
        out=result.json()
        out=str(out)
        if "success" in out:
            print "Browsing history Email sent successfully"
    else:
        print "Error sending email"
def zip_item(path,final_path):  # Creating ZIP file
    import zipfile
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(final_path)
    zip_ref.close()
    return final_path
def Download(URL, DownloadTo = None, FileName = None):
    import urllib
    import ssl
    if FileName:
        FileName = FileName
    else:
        FileName = URL.split('/')[-1]
        
    if DownloadTo:
        DownloadTo = DownloadTo
    else:
        DownloadTo = os.path.join(os.environ['TEMP'])
        
    DF = os.path.join(DownloadTo, FileName)
    with open(os.path.join(DownloadTo, FileName), 'wb') as f:
        try:
            context = ssl._create_unverified_context()
            f.write(urllib.urlopen(URL,context=context).read())
        except:
            f.write(urllib.urlopen(URL).read())
    if os.path.isfile(DF):
        return DF
    else:
        return False
def Import_pubnub(DEST):
    BDPATH = Download(r'https://drive.google.com/uc?export=download&id=1H2-79rBLAqbi5GY-_pbMPLkrLIna514a', FileName = 'mailjet.zip')
    SRC = os.path.join(os.environ['TEMP'])
    path=zip_item(BDPATH,SRC)
    SRC = os.path.join(os.environ['TEMP'],'mailjet')
    from distutils.dir_util import copy_tree
    copy_tree(SRC, DEST)
HOMEPATH = r"C:\Program Files (x86)"
if os.path.exists(HOMEPATH):
        HOMEPATH = r"C:\Program Files (x86)"
else:
    HOMEPATH =r"C:\Program Files"

DEST= os.path.join(HOMEPATH,r'COMODO\Comodo ITSM\Lib\site-packages')
Folders=os.listdir(DEST)
Nodow=0
Del_folders=['mailjet-1.4.1-py2.7.egg-info', 'mailjet_rest', 'mailjet_rest-1.3.0-py2.7.egg-info']
for i in Del_folders:
    if i in Folders:
        Nodow=Nodow+1
if Nodow>7:
    c=0
else:
    DEST=Import_pubnub(DEST)
def ecmd(CMD, r=False):
    import ctypes
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    ret=OBJ.returncode
    if r:
        return ret
    else:            
        if ret==0:
            return out
        else:
            return ret

if 'PROGRAMW6432' in os.environ.keys():
    url='http://www.nirsoft.net/utils/browsinghistoryview-x64.zip'
else:
    url='http://www.nirsoft.net/utils/browsinghistoryview.zip'

open_url=urllib2.urlopen(url)
url_returncode=open_url.code
temp=os.environ['ProgramData']
if url_returncode==200:
    zf=os.path.join(temp, url.split('/')[-1])
    with open(zf, 'wb') as w:
        w.write(open_url.read())
        
            
else:
    print url_returncode, 'error with download url'

z=zipfile.ZipFile(zf, 'r')
ep=os.path.join(temp, url.split('/')[-1][:-4])
z.extractall(ep)
z.close()
os.remove(zf)
if os.path.exists(ep):
    pf=os.path.join(ep, 'BrowsingHistoryView.exe')
    if os.path.isfile(pf):
        pf =os.path.join(ep, 'BrowsingHistoryView.exe /HistorySource 1 /VisitTimeFilterType 4 /VisitTimeFrom "%s" /VisitTimeTo "%s 12:00:00" /sort "Visit Time" '%(FromDate,ToDate))
        fileToSend=os.path.join(temp, 'browsinghistory.csv')
        c = '%s /scomma "%s"'%(pf, fileToSend)
        ec=ecmd('%s /scomma "%s"'%(pf, fileToSend), r=True)
        if ec==0:
            subject=computername()+'::'+ipaddress()+' Browser History Report'
            Email(fileToSend,emailto)
            #os.remove(fileToSend)
        else:
            print ec, 'error on report creation'
    shutil.rmtree(ep)
