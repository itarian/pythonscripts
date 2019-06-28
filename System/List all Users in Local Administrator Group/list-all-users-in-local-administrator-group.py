import ctypes
import os
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

s=[]
Obj = os.popen('net localgroup administrators').read()
for i in [i.strip() for i in Obj.split('\n')  if i.strip()]:
    s.append(i)
      
a=s[4:]
b=("\n".join(a))
print 'Following users in local administrator group:'
print b


    
