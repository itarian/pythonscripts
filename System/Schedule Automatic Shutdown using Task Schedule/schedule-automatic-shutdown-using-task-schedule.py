daily="DAILY"   #Eg:DAILY,MON,TUE,WED,THU,FRI,SAT,SUN
time="20:00"    #TIME-should be in 24 hour format

import os
import subprocess
import socket
from ctypes import *


class disable_file_system_redirection:
    _disable = windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value =c_long()
        self.success = self._disable(byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
            

command='shutdown -s ' 
def command1(daily,time,command):
    path=os.environ['PROGRAMDATA']
    command='"'+command+'"'
    if  os.path.exists(path):
        os.chdir(path)
        with open("command.bat","w+") as f:
            f.write('start cmd.exe /k '+command)
            f.close()

    cmd='schtasks  /ru "SYSTEM"  /create /tn:shutdown /tr:'+path+"\command.bat /sc:"+daily+" /st:"+time+" /f"
    with disable_file_system_redirection(): 
        ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out = ping.communicate()
        if len(out[0])>0:
            print "Task Scheduler Scheduled to restart system at "+time
        else:
            print "Error in task scheduler.Please check your parameters"


command1(daily,time,command)
