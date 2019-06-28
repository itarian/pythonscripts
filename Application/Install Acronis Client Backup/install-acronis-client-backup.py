import os
if os.path.exists("C:\Program Files (x86)"):
    URL=r"https://onedrive.live.com/download?cid=A910C8EF113350FB&resid=A910C8EF113350FB%21125&authkey=AILMqpav6sj04k4" #provide a URL of 64 bit package
else:
    URL=r"https://onedrive.live.com/download?cid=A910C8EF113350FB&resid=A910C8EF113350FB%21126&authkey=ANE-BKFhl8mVaMY" #provide a URL of 32 bit package
import ctypes
import re
import time
import socket
import _winreg
import platform
import shutil
import ssl
import urllib2
import getpass
import zipfile
import shutil
def Download(src_path, URL,fp):
    import urllib2
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        parsed = urllib2.urlopen(request,context=gcontext)
    except:
        parsed = urllib2.urlopen(request)
    if not os.path.exists(src_path):
        os.makedirs(src_path)
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    return fp
Folder=os.environ['programdata']+r"\Acronis_install"
if not os.path.exists(Folder):
    os.mkdir(Folder)
fileName=r"Acronis_install.zip"
src_path=Folder
fp = os.path.join(src_path, fileName)    
Excutable_path=Download(Folder, URL,fp)
print "Downloaded succesfully to "+Excutable_path+""
dest_path=os.environ['programdata']+r"\Acronis_install"
def filezip(Excutable_path,dest_path):
    with zipfile.ZipFile(Excutable_path,"r") as zip_ref:
        zip_ref.extractall(dest_path)
        print 'file unzipped to ' +dest_path 
filezip(Excutable_path,dest_path)
def install():
    k=os.listdir(src_path)
    for i in k:
        if not '.zip' in i:
            des_path=dest_path+"\\"+"%s"%i
            des_fname="BackupClient.msi"
            des_pname="BackupClient.msi.mst"
            des_tname="BackupClient64.msi"
            des_sname="BackupClient64.msi.mst"
            path= des_path+'\\'+des_fname
            path1= des_path+'\\'+des_pname    
            path_x64=des_path+'\\'+des_tname
            x64_path=des_path+'\\'+des_sname
            if os.path.exists("C:\Program Files (x86)"):
                command1='msiexec /i  "'+path_x64+'" /qn  TRANSFORMS="'+x64_path+'" '
                
            else:
                command1='msiexec /i  "'+path+'" /qn  TRANSFORMS="'+path1+'" '
                
            command=os.popen(command1).read()
            print "Acronics backup successfully installed :-)"
install()
try:
    os.chmod(dest_path,0664)
    shutil.rmtree(dest_path)
except:
    pass
