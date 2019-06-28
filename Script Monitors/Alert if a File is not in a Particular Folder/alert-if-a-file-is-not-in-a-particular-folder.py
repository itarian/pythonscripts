import os
import ctypes
import sys

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

path=r'C:\Users\shinchan\Desktop\folder'               #Provide the path of the folder 
file1='abc.exe'                                        #Provide the file name
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

    for File in os.listdir(path):
        if File == file1:
            b=0
            break
        else:
            b=1

if b==0:
    print "file  "+file1+"  exists"
    alert(0)
else:
    print "file  "+file1+"  does not exists"
    alert(1)
