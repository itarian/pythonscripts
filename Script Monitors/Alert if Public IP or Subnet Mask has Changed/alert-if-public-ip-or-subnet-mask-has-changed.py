Public_IP="***************"     # Enter the Public IP address which with you want to compare
Subnet_mask="*************"     # Enter the Subnet mask which with you want to compare

import os
import subprocess
from subprocess import *
import re
import sys
cmd="nslookup myip.opendns.com. resolver1.opendns.com"
cmd1="ipconfig /all"
IP=[]
subnet=[]
al=0

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))

   
try:
    wd=os.environ['PROGRAMDATA']+'\temp'
    if not os.path.exists(wd):
        os.mkdir(wd)
except:
    wd=os.environ['SYSTEMDRIVE']


def check(cmd):
    obj=subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr = PIPE)
    out, err = obj.communicate()
    return out

def compare():
    if IP[0]!=Public_IP or subnet[0]!=Subnet_mask:
        al=1
    else:
        al=0
    return al
    

    
fe=check(cmd)
if fe:
    gt=re.findall('Name:(.*)\s\s\s\smyip.opendns.com\r\n(.*)', fe)
    ge=re.findall('Address:(.*)', gt[0][1])
    IP.append(ge[0].strip())

fr=check(cmd1)
if fr:
    gt=re.findall('Subnet\sMask\s.\s.\s.\s.\s.\s.\s.\s.\s.\s.\s.\s:\s(.*)',fr)
    subnet.append(gt[0].strip())


if IP and subnet:
    st=compare()
    if st>0:
        print "System Public IP or Subnet mask has been changed"
        alert(1)
    else:
        print "System Public IP & Subnet mask is same as specified"
        alert(0)
    
