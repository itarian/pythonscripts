port number="54412" # Give your port number which you want to close

import os
import re
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


                

cmd1="netstat -a -n -o|findstr %s"%inp
with disable_file_system_redirection():
    k=os.popen(cmd1).read()
if len(k)>0:
    k=re.sub("\s+", ",", k.strip())
    k=k.replace(","," ")
    k=k.split(" ")
    cmd2="taskkill /F /PID %s"%k[-1]

    with disable_file_system_redirection():
        op2=os.popen(cmd2).read()
    print op2
    print "This "+inp+" port is successfully closed"

else:
    print "This "+inp+" port is already closed"

















