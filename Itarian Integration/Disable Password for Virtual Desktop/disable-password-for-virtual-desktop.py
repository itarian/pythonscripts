# -*- coding: utf-8 -*-
import codecs
import io
import os
import re
import ctypes
import time
import subprocess
from subprocess import PIPE, Popen
import sys

try:
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)      
except:
    workdir=os.environ['SYTEMDRIVE']


content=r'''<?xml version="1.0"?>
<CisConfigure>
  <df.sandbox.VirtKioskProtect password='' enabled="false"/>
</CisConfigure>'''

        
def create_XML():
    import os
    script =content
    print "Creating XML File\n"

    with open(workdir+r'\Virtual_Desktop.txt',"wb") as f :
        f.write(script)

    sourceEncoding = "iso-8859-1"
    targetEncoding = "utf-8"
    source = open(workdir+r'\Virtual_Desktop.txt')
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
        
    print "Disabled Password for Virtual Desktop"
    
    try:
        if os.path.isfile(workdir+r'\Virtual_Desktop.xml'):
            os.remove(workdir+r'\Virtual_Desktop.xml')
    
    except:
        pass

    
create_XML()
run_cmd()
