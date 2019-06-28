threshold_time =10   # should be less than 60 
import subprocess
from ctypes import *

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return int(millis / 1000.0)

class disable_file_system_redirection:
    _disable = windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value =c_long()
        self.success = self._disable(byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

seconds=get_idle_duration()

m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
d,h =divmod(h,24)

print("System Idle time in DAYS:HOURS:MIN:SEC")
print "%02d:%02d:%02d:%02d" % (d, h, m, s)

if ( m>threshold_time or  h>0):
    with disable_file_system_redirection():          
        ping = subprocess.Popen("rundll32.exe user32.dll, LockWorkStation",stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out = ping.communicate()[0]
        output = str(out)
        print output
        print 'System has been locked'
        


    
