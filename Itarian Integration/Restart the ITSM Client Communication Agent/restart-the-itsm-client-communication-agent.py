import os

instruction="""
Dim sCmd1
Dim sCmd2
Dim WshShell
Set WshShell = WScript.CreateObject("WScript.Shell")
sCmd1="net stop ITSMService" 
sCmd2="net start ITSMService" 
WshShell.Run sCmd1,0, True
WScript.Sleep 3
WshShell.Run sCmd2,0, True
"""

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


temp=os.environ['TEMP']
vbsfile=temp+r'\itsm_restart.vbs'
fobj= open(vbsfile, "w");
fobj.write(instruction)
fobj.close()

with disable_file_system_redirection():
    print os.popen('cscript.exe '+vbsfile).read()
