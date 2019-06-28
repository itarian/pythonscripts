alert_nobackup_days=2
import ctypes
import sys
import time
import socket
import re
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
    
def alert(arg): 
	sys.stderr.write("%d%d%d" % (arg, arg, arg)) 
import os
import re

def check ():
    Insta=ki=os.popen('wmic product where "Name like "%Veeam%"" get Name, Version').read()
    le=re.findall('Veeam',Insta)
    if len(le)>0:
        print "veeam agent is installed on end point "
        return 1
    else :
        print "Veeam agent has not installed ignore the output "
        return 0
ki1=check ()
if ki1 ==1:
    name=os.environ['username']
    print 'PC-NAME : '+name
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print "IP-ADDRESS : " + (s.getsockname()[0])
    with disable_file_system_redirection():
        ki=os.popen('wevtutil qe "Veeam Agent" /q:*[System[(EventID=190)]] /f:text /rd:true /c:1').read()
        
    if ki=='':
        print "Veeam backup has not occured in this device"
        alert(0)
    else:
        sam=re.findall('Date:(.*)',ki)[0]
        time_backup=re.findall('(.*)T',sam)[0]
        time_backup=time_backup.strip(' ')
        time_now=time.strftime('%Y-%m-%d')
        from datetime import datetime
        date_format = "%Y-%m-%d"
        a = datetime.strptime(time_backup, date_format)
        b = datetime.strptime(time_now, date_format)
        delta = b - a
        ki2=alert_nobackup_days

    
    if "finished" in ki:
        
        if delta.days >=ki2 :
            print "There are no backup event from the past "+ str(delta.days) + "days"
            alert(1)
        else:
            print "Successfull backup for Veeam Agent at" + sam
            alert(0)
else:
    alert(0)
