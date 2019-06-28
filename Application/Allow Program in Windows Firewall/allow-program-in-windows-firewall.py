path=itsm.getParameter("Enter_the_path")#Please mention the file path of the program needed to be allowed
name=itsm.getParameter("Enter_the_rule")#Provide any rule name 

import os
import ctypes
import platform

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

    cmd=os.popen('netsh advfirewall firewall add rule name="%s" dir=in program="%s" action=allow'%(name,path)).read()
    print cmd
    if "Ok" in cmd:
    	print "The application is successfully allowed through the windows firewall"
path="C:\Program Files\Mozilla Firefox\firefox.exe"#Please mention the file path of the program needed to be allowed
name="allow"#Provide any rule name 

import os
import ctypes
import platform

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

    cmd=os.popen('netsh advfirewall firewall add rule name="%s" dir=in program="%s" action=allow'%(name,path)).read()
    print cmd
    if "Ok" in cmd:
    	print "The application is successfully allowed through the windows firewall"
