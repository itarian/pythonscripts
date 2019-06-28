sFolder=r'SHARED FOLDER PATH HERE'            ## provide the valid network path here, Example: '\\C1-EN03\kupido
sFolder2=r'%WINDIR%\System32\Printing_Admin_Scripts\en-US'
sUN=r'USER NAME HERE'                     ## provide server username here, Example pattern: domain\username
sPWD=r'PASSWORD HERE'                        ## provide server password here
##VB script Commands are below
command1='cscript "C:\Scripts\Prnmngr.vbs" -d -p "PHS - Online"'
command2='Cscript "C:\Scripts\Prnport.vbs" -a -r IP_192.168.30.38 -h 192.168.30.38 -o raw -n 9100'
command3='Cscript "C:\Scripts\Prndrvr.vbs" -a -m "Ricoh Copy Room Printer" -i C:\DRIVERS2\Ricoh\disk1\oemsetup.inf -h C:\DRIVERS2'
command4='Cscript "C:\Scripts\Prnmngr.vbs" -a -p "PHS - Online" -m "Ricoh Copy Room Printer" -r IP_192.168.30.38'
import time
import os
import ctypes
import shutil
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def ExecuteCMD(CMD, OUT = False):

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

def CopyDriversscripts():

    DS='xcopy "'+sFolder+'" C:\DRIVERS2 /i /y /d'

    DS1='xcopy "'+sFolder2+'" C:\Scripts /i /y /d'
    if ExecuteCMD(AS):        
        ExecuteCMD(DS)
        ExecuteCMD(DS1)
        print "Shared Folder Access is Successfull"
        print "Copying Drivers"
        print "Copying Vb Scripts"
    else:
        print 'the path '+sFolder+' is not accessible by the credential, username:'+sUN+' and password:'+sPWD+' :('
def Excutedriver():
    print "Running VBSCRIPTS"
    ExecuteCMD(command1)
    time.sleep(1)
    ExecuteCMD(command2)
    time.sleep(1)
    ExecuteCMD(command3)
    time.sleep(1)
    ExecuteCMD(command4)
    time.sleep(1)

AS=r'net use '+sFolder+' /user:'+sUN+' '+sPWD+' /P:No'
CopyDriversscripts()
Excutedriver()
if os.path.isdir("C:\DRIVERS2"):
    shutil.rmtree("C:\DRIVERS2")
    print "Driver folder is deleted"
if os.path.isdir("C:\Scripts"):
    shutil.rmtree("C:\Scripts")
    print "Script Folder is deleted"
