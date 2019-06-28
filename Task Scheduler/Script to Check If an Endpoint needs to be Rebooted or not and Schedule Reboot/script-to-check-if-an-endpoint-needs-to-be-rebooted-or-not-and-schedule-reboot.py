run_as_username='john'# Please edit with your username 
run_as_password='comodo' #Please edit with your password
task_name='task name Reboot' 
hour_at="03" #Edit with the hour and minutes to schedule
minute_at="00"

import subprocess
import ctypes

def ecmd(CMD, OUT=False):
    import ctypes
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    return out.strip()


def wfile(fp, c):
    import os
    with open(fp, 'w') as f:
        f.write(c)
    if os.path.isfile(fp):
        return fp
    return

import os
import time
import socket
c=r'''Set objSysInfo = CreateObject("Microsoft.Update.SystemInfo")
Wscript.Echo "Reboot required? " & objSysInfo.RebootRequired'''

fp=os.path.join(os.environ['TEMP'], 'RebootRequired.vbs')
file=wfile(fp, c)
vbsout=ecmd('cscript "'+file+'"')
tim=time.strftime('%d/%m/%Y %H:%M')
cn=os.environ['COMPUTERNAME']
ip=socket.gethostbyname(socket.gethostname())
print 'Date and Time:', tim
print 'Machine Info:', cn+' - '+ip
print '-'*40+'\n'
if 'Reboot required? False' not in vbsout:
    print 'The endpoint do not require reboot :)'
elif 'Reboot required? True' in vbsout:
    with disable_file_system_redirection():
        CMD=r'schtasks /create /ru %s /rp %s /tn "%s" /tr "shutdown /r /t 1" /sc once /st %s:%s /f'%(run_as_username, run_as_password, task_name, hour_at, minute_at)
        print CMD
        print 'The endpoint require reboot :(.\nSo please reboot as soon as possible\n'
    process= subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE)
    result=process.communicate()
    ret=process.returncode
    if ret==0:
        if result[0]:
            print result[0].strip()
        else:
            print result[0]
    else:
        if result[1]:
            print result[1].strip()
        else:
            print result[1]


else:
    print vbsout+'\n'

os.remove(file)
   
