import os
import ctypes
import sys
service=[ "gupdate","cmdAgent"]# Enter your own service here
ale=0
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
with disable_file_system_redirection():
    out=os.popen("wmic service where startmode='Auto' get name, startmode, state | find "'"Stopped"'"").read();
for i in service:
   if i in out:
      if out:
         print i+" is in stopped state"
         ale=ale+1
      
if ale>1:
   alert(1)
else:
   print "some specified application is not in stopped state"
   alert(0)
