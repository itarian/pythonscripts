import os
import sys
import platform
import subprocess
import ctypes
import re

s=''

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


def disc():
    with disable_file_system_redirection():
        result=''
        f=0
        detected_drives=os.popen("wmic logicaldisk get name").read()
        required_drive_letters=[i.strip() for i in detected_drives.split('\n') if i.strip()][1:]
        if required_drive_letters:
            for i in required_drive_letters:
                other_drive_fix=os.popen('chkdsk %s'%i).read()
                trimed_other_drive_fix=''
                if other_drive_fix:
                    for a in other_drive_fix.split('\r'):
                        if 'progress' not in a.lower() and 'percent' not in a.lower():
                                if a.strip():
                                        trimed_other_drive_fix+=a
                if "Windows found problems with the file system." in trimed_other_drive_fix:
                    f=f+1
                    
        if f>0:
            print 'Windows found problems with the file system '
            alert(1)
        else:
            print 'Windows has checked the file system and found no problems'
            alert(0)

        sd=os.popen("echo y|chkdsk /f /r ").read()
        print '\n',sd   
        

d=os.popen('systeminfo').read()
get=re.findall('OS Name:(.*)',d)
s=''.join(get)
s=s.strip()

if 'Microsoft Windows' in s:
    disc()
else:
    print "The system has Multiple Hard Disk Drive, Couldn't proceed this process"
    
