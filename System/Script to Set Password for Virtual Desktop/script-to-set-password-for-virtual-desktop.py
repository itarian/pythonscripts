# -*- coding: utf-8 -*-
Password="aravindpandi"  # Enter the password as String

import codecs
import hashlib
import io
import os
import re
import ctypes
import time
import subprocess
from subprocess import PIPE, Popen
import sys
string=''
val=''


try:
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)      
except:
    workdir=os.environ['SYTEMDRIVE']

        
def create_SHA1():
    import os
    print "Creating SHA1\n"

    with open(workdir+r'\Virtual_Desktop.txt',"wb") as f :
        f.write(Password)

    sourceEncoding = "utf-8"
    targetEncoding = "utf-16-le"
    source = open(workdir+r'\Virtual_Desktop.txt')
    target = open(workdir+r'\Virtual_Desktop1.txt', "w")

    target.write(unicode(source.read(), sourceEncoding).encode(targetEncoding))
    s=workdir+r'\Virtual_Desktop1.txt'

    sourceEncoding = "utf-8"
    targetEncoding = "utf-16-le"
    source = open(workdir+r'\Virtual_Desktop.txt')
    target = open(workdir+r'\Virtual_Desktop1.txt', "r")
    if target:
        string=target.readline()


    d = hashlib.sha1(string)
    val=d.hexdigest()
    print val
    print "\nSHA1 is created for given string\n"
    return val



content=r'''<?xml version="1.0"?>
<CisConfigure>
  <df.sandbox.VirtKioskProtect password="%s" enabled="true"/>
</CisConfigure>'''
        
def create_XML(SHA1):
    
    import os
    script =content %(SHA1)
    print "Creating XML File"

    with open(workdir+r'\Virtual.txt',"wb") as f :
        f.write(script)

    sourceEncoding = "iso-8859-1"
    targetEncoding = "utf-8"
    source = open(workdir+r'\Virtual.txt')
    target = open(workdir+r'\Virtual_Desktop.xml', "w")

    target.write(unicode(source.read(), sourceEncoding).encode(targetEncoding))

          

    if os.path.exists(workdir+r'\Virtual_Desktop.xml'):
        print "XML file has created\n"
    else:
        print "XML file has not created"


def run_cmd():
    os.chdir("C:\Program Files\COMODO\COMODO Internet Security")
    obj=os.popen('cfpconfg.exe --xcfgMerge "'+workdir+'\Virtual_Desktop.xml"').read()
    
    print obj
        
    print "Created Password for Virtual Desktop"
    
    try:
        if os.path.isfile(workdir+r'\Virtual_Desktop.xml'):
            os.remove(workdir+r'\Virtual_Desktop.xml')
    
    except:
        pass

    
SHA1=create_SHA1()
create_XML(SHA1)
run_cmd()

