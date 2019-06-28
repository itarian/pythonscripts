from __future__ import division
import os
import re
import ctypes
import math


class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)

file_path=r"C:\Windows\System32\winevt\Logs\Security.evtx"

with disable_file_system_redirection():

    def file_size(file_path):
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            a=file_info.st_size
            one=long(a)
            

            try:
                b=os.popen('wevtutil gl Security |find "maxSize"').read()
                x=b.split(" ")[-1]
                x=long(x)
                
            except:
                x=long(20480000)
                
            two=long(x)
            result=float(one/two)
            ki=int(100*result)
            print "Security log file is used "+str(ki)+" percentage"

b=file_size(file_path)


