sFolder=r'\\xyz\script' ## provide the valid network path here, Example: \\fs2.ch.office.comodo.net\Common\C4
sUN=r'xyz' ## provide server username here, Example pattern: domain\username
sPWD=r'comodo' ## provide server password here
sFile='file.txt' ## file name to be written with [if no file exist then create new file on the given name], Example: filename.txt
Command=r'ipconfig' ## command you want to execute, if you would like to run the PowerShell command then use the notation 'powershell "PowerShell commands"'. Example: powershell "Get-WmiObject -Class Win32_Processor -ComputerName ."

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
    if RET==0:
        if OUT:
            if out:
                return out.strip()
            return True
        return True
    return False

def writeText(file, str):
    with open(file, 'a') as f:
        f.write(str)

import time
import os
sPath=os.path.join(sFolder, sFile)
AS=r'net use '+sFolder+r' /user:'+sUN+r' '+sPWD+r' /P:No'
if ExecuteCMD(AS):
    writeText(sPath, '='*5+os.environ['computername']+' start time: '+time.strftime("%d/%m/%Y")+' '+time.strftime("%H:%M:%S")+'='*5+'\n')
    str=ExecuteCMD(Command, True)
    writeText(sPath, str+'\n')
    DS=r'net use '+sFolder+r' /delete'
    writeText(sPath, '='*5+os.environ['computername']+' end time: '+time.strftime("%d/%m/%Y")+' '+time.strftime("%H:%M:%S")+'='*5+'\n\n')
    ExecuteCMD(DS)
    print 'command executed successfully :)\ncheck the output file at: '+sPath
else:
    print 'the path '+sFolder+' is not accessible by the credential, username:'+sUN+' and password:'+sPWD+' :('
