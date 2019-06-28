VBScr = '''Dim WshShell, BtnCode
Set WshShell = WScript.CreateObject("WScript.Shell")
BtnCode = WshShell.Popup("Computer will reboot in 2 minutes. Do you want to continue?", 120, "Administrator Required Reboot:", 4 + 32)
If BtnCode=6 Then
    strShutdown = "shutdown.exe -r -t 120 -f"
    Set objShell = CreateObject("WScript.Shell")
    objShell.Run strShutdown, 0, False
ElseIf BtnCode=7 Then
    WScript.Echo 1
Else
    WScript.Echo 2
End If'''

import os
FILEPATH = os.path.join(os.environ['TEMP'], 'vbscript.vbs')
with open(FILEPATH, 'w') as f:
    f.write(VBScr)
    
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

def SeOutput(Pat, Str):
    import re
    se = re.search(Pat, Str)
    if se:
        return int(se.group().strip())
    else:
        return False

if os.path.isfile(FILEPATH):
    OUTPUT = ExecuteCMD('cscript "'+FILEPATH+'"', True)
    UserRes = SeOutput(r'[\r\n]+[0-9]', OUTPUT)
    if UserRes == 1:
        raise Exception("User did not allow the reboot")
    elif UserRes == 2:
        raise Exception("User did not response the alert")
    else:
        print 'Success: User allowed the reboot'
        
os.remove(FILEPATH)
