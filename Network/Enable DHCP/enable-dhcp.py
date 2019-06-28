import os
import ctypes
import re
import shutil
vbs1=r'''
strComputer = "." 
Set objWMIService = GetObject("winmgmts:" _ 
    & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2") 
 
Set colNetAdapters = objWMIService.ExecQuery _ 
    ("Select * from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE") 
  
For Each objNetAdapter In colNetAdapters 
    errEnable = objNetAdapter.EnableDHCP() 
Next 
'''
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
    cmd=os.popen('ipconfig /all').read()
    a=re.search("DHCP Enabled. . . . . . . . . . . : Yes",cmd)
    if a:
        print "DHCP is already enabled in this interface"
    else:
        workdir=os.environ['PROGRAMDATA']+r'\temp'
        if not os.path.exists(workdir): 
            os.makedirs(workdir)
        with open(workdir+r'\temprun.vbs',"w") as f :
            f.write(vbs1)
        print os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
        print('DHCP .........Enabled')
        if os.path.exists(workdir):
            shutil.rmtree(workdir)

