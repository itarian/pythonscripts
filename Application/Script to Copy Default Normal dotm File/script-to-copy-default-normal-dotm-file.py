sec=1800 #mention time for the prompt in sec (30min = 1800sec)
src_path=r'\\WIN-BIKTODGSCBO\New folder2'  #source folder path need to be copied 
share_path=r'C:\Users\assassin\AppData\Roaming\Microsoft\Templates'  # Destination share path
fname='\\Normal.dotm'   # please provide the name of the .dotm file need to be copied
share_user="Administrator"  # share path user name 
share_pass="comodo@123" #share path password
import os
import shutil
import ctypes
import subprocess
import sys
from Tkinter import *
from shutil import copyfile
import sys 
import ctypes
from threading import Timer
import time
import re
import _winreg
from os import listdir
a= os.environ['USERNAME']
class disable_file_system_redirection:
    
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
import ctypes
from Tkinter import *
import os

def share():
    cmd='NET USE "'+src_path+'" /USER:'+share_user+'  "'+share_pass+'"'
    print cmd
    tar_path=share_path+'\\'+fname
    print tar_path
    print 'Login to network share'
    with disable_file_system_redirection():
        print os.popen(cmd).read()

    print 'Copying files to local machine....'

    if os.path.isdir(src_path):
            shutil.copy2(src_path + fname,tar_path)
            print 'Script execution completed successfully'

    else:
            print '%s is not found'%src_path
    
def hold():
    time.sleep(sec)
    msg()

def msg():
    title=u"Microsoft OUTLOOK and WORD will be closed for copying new custom macros, to continue click YES " ## Define your message here 
    message=u"Message from: ADMINISTRATOR" 
    ki=ctypes.windll.user32.MessageBoxW(None,title, message, 4)
    if ki==6:
        print "User said YES"
        cmd=os.popen('taskkill /F /IM OUTLOOK.EXE').read()
        cmd1=os.popen('taskkill /F /IM WINWORD.EXE').read()
        share()
    
    elif ki == 7:
        print "User said NO"
        hold()

msg()

