import os
import ctypes
import re
import time
import sys

a=0

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

   
def check():
    with disable_file_system_redirection():
        inst=os.popen("wmic product get name,identifyingnumber").read()
         
    return inst
        

inst=check()
 
if len(inst)>0:
    find=re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity',inst)
    if len(find)>0:
        final=re.findall('{.*}',find[0])[0]
        if len(final) >0:
            a=1
   

   
if a ==1:
    
    print "COMODO Client Security  is installed on Endpoint"
    alert(0)
else:
    print "Comodo Client Security is not installed at End point"
    alert(1)
