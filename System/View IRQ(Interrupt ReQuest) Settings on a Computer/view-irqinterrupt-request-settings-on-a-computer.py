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
IRGVBScript=r'''' Enumerating IRQ Settings
On Error Resume Next
strComputer = "."
Set objWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")
Set colItems = objWMIService.ExecQuery("Select * from Win32_IRQResource")
For Each objItem in colItems
    Wscript.Echo "Availability: " & objItem.Availability
    Wscript.Echo "Hardware: " & objItem.Hardware
    Wscript.Echo "IRQ Number: " & objItem.IRQNumber
    Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "Trigger Level: " & objItem.TriggerLevel
    Wscript.Echo "Trigger Type: " & objItem.TriggerType
    Wscript.Echo
Next'''

file=writeFile(IRGVBScript, '.vbs')
import os
if os.path.isfile(file):
    print ExecuteCMD('cscript "'+file+'"', True)

## cleans up the vbs script file
os.remove(file)
