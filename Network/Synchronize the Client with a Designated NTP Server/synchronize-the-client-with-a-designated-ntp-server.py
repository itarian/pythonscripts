yourtimerserver="*****" #enter your timeserver here
import os
import ctypes
import time
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
def main(cmd):
    with disable_file_system_redirection():
        cmd1=os.popen(cmd).read()
        return cmd1
c="w32tm /unregister"
main(c)
c1="net stop w32time"
main(c1)
a="w32tm /register"
main(a)
b="net start w32time"
main(b)
d="w32tm /config /manualpeerlist:%s /syncfromflags:manual /reliable:yes /update" %(yourtimerserver)
main(d)
f="w32tm /query /peers"
e=main(f)
if "NTP" in e:
    print "Synchronized with NTP"
else:
    g="w32tm /config /manualpeerlist:pool.ntp.org /syncfromflags:manual /reliable:yes /update" 
    g1=main(g)
    time.sleep(10)
    g2=main(f)
    if "NTP" in g2:
        print "Synchronized with NTP"
    else:
        print "Not Synchronized" 
