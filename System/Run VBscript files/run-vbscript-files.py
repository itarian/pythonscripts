vbs=r'''
Dim sCmd1
Dim sCmd2
Dim sCmd3
Dim WshShell
sCmd1="wmic product where name=""RMM Agent Service"" call uninstall"
Set WshShell = WScript.CreateObject("WScript.Shell")
WshShell.Run sCmd1,0, True
WScript.Sleep 10
'''
import os
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


def runvbs(vbs):
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.isdir(workdir): 
        os.mkdir(workdir)
    with open(workdir+r'\temprun.vbs',"w") as f :
        f.write(vbs)        
    with disable_file_system_redirection():
        print os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
        print('Script execution completed successfully')
    if os.path.isfile(workdir+r'\temprun.vbs'):
        os.remove(workdir+r'\temprun.vbs')

runvbs(vbs) 

