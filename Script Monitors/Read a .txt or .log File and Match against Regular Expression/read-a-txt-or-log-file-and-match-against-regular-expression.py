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



f =open('C:/Users/Nyle/Desktop/1234.txt', 'r')  #provide the path of the .txt or .log file here
filetext = f.read()
f.close()
matches = re.findall("(<(\d{4,5})>)?" , filetext)
if matches==[]:
   a=0
else:
   a=1

if a ==1:
    print "Regex matched successfully"
    alert(1)
else:
    print "Regex not matched "
    alert(0)
    


