OfficeClientEdition="32" #Installs the edition of office
Channel="Targeted" #Installs the Office installation files from Semi-Annual Channel
Product_ID="O365ProPlusRetail" #Installs Office 365 ProPlus
Language_ID="en-us" #Installs English version of Office 
Display_Level="None" #Displays the installation progress
fil=""" <Configuration> 
  <Add OfficeClientEdition="%s" 
       Channel="%s"> 
   <Product ID="%s" > 
     <Language ID="%s" />      
   </Product> 
  </Add> 
  <Display Level="%s" 
           AcceptEULA="TRUE" />
</Configuration>"""%(OfficeClientEdition, Channel, Product_ID, Language_ID, Display_Level )

import shutil
import ctypes
import sys
import platform
import _winreg
import ssl
import shutil
import os
import urllib2
import subprocess

ssl._create_default_https_context = ssl._create_unverified_context
temp=os.environ['PROGRAMDATA']+r'\c1_temp'
check="C:\Program Files (x86)\Microsoft Office\Office16"
check1="C:\Program Files\Microsoft Office\Office16"

if not os.path.exists(temp):
    os.makedirs(temp)

url=r'https://download.microsoft.com/download/2/7/A/27AF1BE6-DD20-4CB4-B154-EBAB8A7D4A7E/officedeploymenttool_8529.3600.exe'
temp_path=os.environ['PROGRAMDATA']+r'\c1_temp'
configuration_file="config-group2-SACT.xml "
config_path=temp_path+'\\'+configuration_file
with open(config_path,"w") as f:
    f.write(fil)

def Download(temp_path,url):
    fileName = 'deployment.exe'
    fp = os.path.join(temp_path, fileName)
    request = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(temp_path):
        pass
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    return fp

def executems():
    os.chdir(temp_path)
    cmd=os.popen("deployment.exe /extract:"+temp_path+ ' /quiet').read()
    print cmd    
    cmd1=("setup.exe /configure %s"%configuration_file)
    ping = subprocess.Popen(cmd1,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
    out=ping.communicate()[1]
    output = str(out)
    print output
    print "Ms office has been successfully deployed on your endpoint"


if 'PROGRAMW6432' in os.environ.keys():
    if os.path.exists(check):
        print "Microsoft Office16 is already installed on your machine "
    else:
        print "Microsoft office installation starts....."
        Download(temp_path,url)
        executems()
        os.chmod(temp_path,0644)
           
else:
    if os.path.exists(check1):
        print "Microsoft Office16 is already installed on your machine "
    else:
        print "Microsoft office installation starts....."
        Download(temp_path,url)
        executems()
        os.chmod(temp_path,0644)
try:
    shutil.rmtree(temp_path)

except:
    pass
