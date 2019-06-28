vbs=r'''
strComputer = "."
 
Set objWMIService = GetObject("winmgmts:" _
    & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\default")

Set objItem = objWMIService.Get("SystemRestore")
errResults = objItem.GetLastRestoreStatus()
 
Select Case errResults
    Case 0 strRestoreStatus = "The last restore failed."
    Case 1 strRestoreStatus = "The last restore was successful."
    Case 2 strRestoreStatus = "The last restore was interrupted."
End Select
 
Wscript.Echo strRestoreStatus
'''
import os
import ctypes
import re
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
def runvbs(vbs):
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.isdir(workdir): 
        os.mkdir(workdir)
    with open(workdir+r'\temprun.vbs',"w") as f :
        f.write(vbs)        
    with disable_file_system_redirection():
        ki=os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
        if len(ki)>107:
            print ki
        else:
            print "No shadow copy items found"
    if os.path.isfile(workdir+r'\temprun.vbs'):
        os.remove(workdir+r'\temprun.vbs')
runvbs(vbs)
