vbs=r'''
strComputer = "."
Set objWMIService = GetObject("winmgmts:" _
    & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")
Set colItems = objWMIService.ExecQuery("Select * from Win32_ShadowCopy")
For Each objItem in colItems
    Wscript.Echo "***********************************"
    Wscript.Echo "ID: " & objItem.ID
    Wscript.Echo "Client accessible: " & objItem.ClientAccessible
    Wscript.Echo "Count: " & objItem.Count
    Wscript.Echo "Device object: " & objItem.DeviceObject
    Wscript.Echo "Differential: " & objItem.Differential
    Wscript.Echo "Exposed locally: " & objItem.ExposedLocally
    Wscript.Echo "Exposed name: " & objItem.ExposedName
    Wscript.Echo "Exposed remotely: " & objItem.ExposedRemotely
    Wscript.Echo "Hardware assisted: " & objItem.HardwareAssisted
    Wscript.Echo "Imported: " & objItem.Imported
    Wscript.Echo "No auto release: " & objItem.NoAutoRelease
    Wscript.Echo "Not surfaced: " & objItem.NotSurfaced
    Wscript.Echo "No writers: " & objItem.NoWriters
    Wscript.Echo "Originating machine: " & objItem.OriginatingMachine
    Wscript.Echo "Persistent: " & objItem.Persistent
    Wscript.Echo "Plex: " & objItem.Plex
    Wscript.Echo "Provider ID: " & objItem.ProviderID
    Wscript.Echo "Service machine: " & objItem.ServiceMachine
    Wscript.Echo "Set ID: " & objItem.SetID
    Wscript.Echo "State: " & objItem.State
    Wscript.Echo "Transportable: " & objItem.Transportable
    Wscript.Echo "Volume name: " & objItem.VolumeName
    Wscript.Echo "***********************************"
    Wscript.Echo
Next
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
