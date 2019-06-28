version_url='http://cmdm.comodo.com/download/win/communication_client/latest/itsm_agent.msi'#please give the url to update the specific version
silent="/qn" #please the give silent installation command
import urllib
import urllib2
import re
import os,sys
import ctypes
import subprocess
import platform

def Download(version_url,silent):
    print "Download started"
    fileName =version_url.split('/')[-1]
    print fileName
    src_path=os.environ['ProgramData']+r'\\'+'c1_temp'
    print  src_path
    fp = os.path.join(src_path, fileName)
    print fp
    request = urllib2.Request(version_url, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(src_path):
        print "Path already exists"
    if not os.path.exists(src_path):
        os.makedirs(src_path)
        print "Path created"
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    print "The file downloaded successfully in specified path"+fp
    try:
        print'Downloaded Application %s Installation Started'%fileName
        os.popen('msiexec /i ' +fp+' '+silent).read()
        
    except:
        return 'No : '+fp+' is exist'

   
Download(version_url,silent)
print "Installed sucessfully"


