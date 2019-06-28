# The script is a template to check UAC status on device. 
import os 
import sys 
import _winreg 

def alert(arg): 
	sys.stderr.write("%d%d%d" % (arg, arg, arg))
	
vbs=r'''
Set objSession = CreateObject("Microsoft.Update.Session")

Set objSearcher = objSession.CreateUpdateSearcher

Set colHistory = objSearcher.QueryHistory(0, 1)


For Each objEntry in colHistory

    Wscript.Echo "Title: " & objEntry.Title

    Wscript.Echo "Update application date: " & objEntry.Date

Next

'''
import os
import ctypes
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


def runvbs(vbs):
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.isdir(workdir): 
        os.mkdir(workdir)
    with open(workdir+r'\temprun.vbs',"w") as f :
        f.write(vbs)        
    with disable_file_system_redirection():
        output=os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
        
    if os.path.isfile(workdir+r'\temprun.vbs'):
        os.remove(workdir+r'\temprun.vbs')
    return output

output=runvbs(vbs)
sam=re.findall("Update\sapplication\sdate:(.*)",output)[0]
sam1=sam.split(' ')[1]
d1=sam1
import platform
ki=platform.platform()
if "Windows-8" in ki:
	print "Win 8"
	f = d1.split("/")
	d1=f[1] + "/" + f[0].rjust(2,"0") + "/" + f[2].rjust(2,"0")
elif "Windows-10" in ki:
    print "win 10"
    if 'PROCESSOR_ARCHITEW6432' in os.environ:
            f = d1.split("/")
            d1=f[1] + "/" + f[0].rjust(2,"0") + "/" + f[2].rjust(2,"0")
    else:
            f = d1.split("/")
            d1=f[0] + "/" + f[1].rjust(2,"0") + "/" + f[2].rjust(2,"0")
	
    
elif "Windows-7" in ki:
    print "windows 7"
    f = d1.split("/")
    d1=f[1] + "/" + f[0].rjust(2,"0") + "/" + f[2].rjust(2,"0")



import time                         
d2=time.strftime("%d/%m/%Y")
from datetime import datetime
date_format = "%d/%m/%Y"
date_format1= "%m/%d/%Y"
if "Windows-10" in ki:
    a = datetime.strptime(d1, date_format1)
    b = datetime.strptime(d2, date_format)
    delta = b - a
else:
    a = datetime.strptime(d1, date_format)
    b = datetime.strptime(d2, date_format)
    delta = b - a
    
print str(delta.days) + " days Since the last update"
if delta.days >=60:
    print "Updates are not working properly"
    alert(1)
else:
    print "Updates are perfectly working"
    alert(0)
