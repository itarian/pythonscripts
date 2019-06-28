Filepath=r'\\TEDDYBEAR-PC\Desktop'                                        ##Provide the network share file path for example: \\TEDDYBEAR-PC\Desktop
share_user="xxxxxxxxx"                                             ## Provide the user name for the shared path
share_pass="yyyyyyyyy"                                               ## Provide the password for the shared path
Setup_Path_X64=r"windows10.0-kb4103714-x64.msu"     ## Enter the .msu file name with extension for 64 bit for example : windows10.0-kb4103714-x64.msu
Setup_Path_X86=r"windows10.0-kb4103714-x86.msu"     ##  Enter the .msu file name with extension for 32 bit for example : windows10.0-kb4103714-x86.msu
kbvalue=r"KB4103714"                                ## Enter the KB value of the update for example: KB4103714

import os
import shutil
import ctypes
import subprocess
import socket
import time
import re
from shutil import copyfile

fileToSend=os.path.join(os.environ['Temp'],'win_update.txt')
a=0

path=r"C:\Program Files (x86)"
if os.path.exists(path):
    NFN=Setup_Path_X64    
else:
    NFN=Setup_Path_X86

    
CP=os.path.join(Filepath,NFN)
workdir=os.environ["TEMP"]
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
            
def login():
    with disable_file_system_redirection():
        cmd= 'NET USE "'+Filepath+'" /USER:'+share_user+'  "'+share_pass+'"'
        print 'Login to network share'
        p= os.popen(cmd).read()
        if p=='':
            print 'Login to network share failed. Provide the accurate credentials'
        else:
            print p
            print 'Copying  file from Network share....'
            print os.popen('copy "'+CP+'" '+workdir).read()
            PTI=os.path.join(workdir,NFN)
            CMD ="wusa.exe "+PTI+" /quiet"
            os.chdir(workdir)
            ab=os.popen(CMD).read()
            print "\n"
            print "The update installed successfully wait for few minutes the system restarts"
    
with disable_file_system_redirection():
    win_update=os.popen(r'wmic qfe list ').read()
    if win_update:
        with open(fileToSend, 'w+') as f:
            f.write(win_update)

    if  os.path.exists(fileToSend):    
        with open (fileToSend, 'r') as file:
            for line in file:
                string=''
                line=line.strip()
                if kbvalue in line:
                    a=1
                    if line=='':
                        continue
                    else:
                       line=line.strip()
                       string+=''.join(line)
                    print string
                    
    if a==1:
        print "\n"
        print "The update "+kbvalue+" is already installed"
        
    else:
        print "\n"
        print "The update "+kbvalue+" is not available"
        login()
