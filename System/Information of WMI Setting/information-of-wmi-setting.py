def skipnulls(pat, out):
    import re
    fout=re.findall(pat, out)
    text=''
    for i in fout:
        text+=i+'\n'
    return text

def ExecuteCMD(CMD, OUT = False):
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
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    RET = OBJ.returncode
    if RET == 0:
        if OUT == True:
            if out != '':
                return out.strip()
            else:
                return True
        else:
            return True
    else:
        return False

def writeFile(con, ext):
    import os
    import random
    FILEPATH = os.path.join(os.environ['TEMP'], str(random.randint(1, 10000))+ext)
    with open(FILEPATH, 'w') as f:
        f.write(con)
    return FILEPATH

## VBScript for Enumerating IRQ Settings
VBScript=r'''On Error Resume Next
strComputer = "."
Set objSWbemLocator = CreateObject("WbemScripting.SWbemLocator")
Set objSWbemServices = objSWbemLocator.ConnectServer(strComputer, "root\cimv2")
Set colSWbemObjectSet = objSWbemServices.InstancesOf("Win32_WMISetting")
For Each objSWbemObject In colSWbemObjectSet
    Wscript.Echo "ASPScriptDefaultNamespace: " & objSWbemObject.ASPScriptDefaultNamespace
    Wscript.Echo "ASPScriptEnabled: " & objSWbemObject.ASPScriptEnabled
    ' WScript.Echo "AutorecoverMofs: " & objSWbemObject.AutorecoverMofs
    Wscript.Echo "AutoStartWin9X: " & objSWbemObject.AutoStartWin9X
    Wscript.Echo "BackupInterval: " & objSWbemObject.BackupInterval
    Wscript.Echo "BackupLastTime: " & objSWbemObject.BackupLastTime
    Wscript.Echo "BuildVersion: " & objSWbemObject.BuildVersion
    WScript.Echo "Caption: " & objSWbemObject.Caption
    Wscript.Echo "DatabaseDirectory: " & objSWbemObject.DatabaseDirectory
    Wscript.Echo "DatabaseMaxSize: " & objSWbemObject.DatabaseMaxSize
    Wscript.Echo "Description: " & objSWbemObject.Description
    Wscript.Echo "EnableAnonWin9xConnections: " & objSWbemObject.EnableAnonWin9xConnections 
    Wscript.Echo "EnableEvents: " & objSWbemObject.EnableEvents 
    Wscript.Echo "EnableStartupHeapPreallocation: " & objSWbemObject.EnableStartupHeapPreallocation 
    Wscript.Echo "HighThresholdOnClientObjects: " & objSWbemObject.HighThresholdOnClientObjects
    Wscript.Echo "HighThresholdOnEvents: " & objSWbemObject.HighThresholdOnEvents  
    Wscript.Echo "InstallationDirectory: " & objSWbemObject.InstallationDirectory 
    Wscript.Echo "LastStartupHeapPreallocation: " & objSWbemObject.LastStartupHeapPreallocation 
    Wscript.Echo "LoggingDirectory: " & objSWbemObject.LoggingDirectory 
    Wscript.Echo "LoggingLevel: " & objSWbemObject.LoggingLevel 
    Wscript.Echo "LowThresholdOnClientObjects: " & objSWbemObject.LowThresholdOnClientObjects 
    Wscript.Echo "LowThresholdOnEvents: " & objSWbemObject.LowThresholdOnEvents 
    Wscript.Echo "MaxLogFileSize: " & objSWbemObject.MaxLogFileSize 
    Wscript.Echo "MaxWaitOnClientObjects: " & objSWbemObject.MaxWaitOnClientObjects 
    Wscript.Echo "MaxWaitOnEvents: " & objSWbemObject.MaxWaitOnEvents 
    Wscript.Echo "MofSelfInstallDirectory: " & objSWbemObject.MofSelfInstallDirectory 
    Wscript.Echo "SettingID: " & objSWbemObject.SettingID
    WScript.Echo
Next'''

file=writeFile(VBScript, '.vbs')
import os
if os.path.isfile(file):
    print skipnulls(r'\S+\:\s\S+',ExecuteCMD('cscript "'+file+'"', True))

## cleans up the vbs script file
os.remove(file)
