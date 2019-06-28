# The script is a template to check UAC status on device.
Max_rp_size=1.0
import os
import sys
import _winreg
drive= os.environ['SystemDrive']
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

# Please use "alert(1)" to turn on the monitor(trigger an alert)
# Please use "alert(0)" to turn off the monitor(disable an alert)
# Please do not change above block and write your script below

import re
import getpass
import socket
def ecmd(CMD, r=True):
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
    ret=OBJ.returncode
    if r:
        return ret
    else:            
        if ret==0:
            return out
        else:
            return ret

print "USER NAME: "+getpass.getuser()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print "IP-ADDRESS : "+(s.getsockname()[0])
from time import gmtime, strftime
time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
print '\n'
def ecmd(CMD, r=False):
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
    ret=OBJ.returncode
    if r:
        return ret
    else:            
        if ret==0:
            return out,ret
        else:
            return err,ret
p,ret1=ecmd('vssadmin list ShadowStorage /For=%s'%drive)
if ret1==1:
    print 'No Restore Points presnet in your system'
    print '\n'
    print 'Creating new Restore Point..........'
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

    ExecuteCMD(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore" /v SystemRestorePointCreationFrequency /t REG_DWORD /d 0 /f')
    print ExecuteCMD(r'WMIC /Namespace:\\root\default Path SystemRestore Call CreateRestorePoint "BY COMODO ITSM %DATE% %TIME%", 100, 12', True)
    ExecuteCMD(r'reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore" /v SystemRestorePointCreationFrequency /f')
    ##print ExecuteCMD(r'POWERSHELL Get-ComputerRestorePoint', True)
    alert(1)
    
else:
    if p is not None:
        reg= re.findall('Used(.*)',p)
        ST=''.join(reg).strip('Shadow Copy Storage space:')
        if 'GB' in ST:
            USED=ST.split(' ')[0]
            Used_rp_size=float(USED)
            if Used_rp_size >= Max_rp_size:
                alert(1)
                print 'USED RESTORE POINT STORAGE SPACE  ' + str(Used_rp_size) + str(ST.split(' ')[1])+ ' IS GREATER THAN THRESHOLD SPACE'
                print '\n'
                print 'For more details:'
                v=os.popen('vssadmin list ShadowStorage /For=%s ' %drive).read()
                info=re.findall('(For\svolume|Shadow\sCopy\sStorage\svolume):(.*)',v)
                for i in range(0,len(info1)):
                    print''.join(info1[i]).replace('\\\\?\\','  ').strip('\\')
                print '\n'
                #date and info
                fin=ecmd('vssadmin list shadows /for=%s ' %drive)
                fin_list=list(fin)
                for f in range(0,len(fin_list)-1):
                    print fin_list[f]  
            else:
                print 'USED RESTORE POINT STORAGE SPACE ' + str(USED)+ str(ST.split(' ')[1]) +' IS LESS THAN THRESHOLD SPACE'
                alert(0)
            
        elif 'MB' in ST:
            USED=ST.split(' ')[0]
            mb_used=float(USED)/1024
            if mb_used >= Max_rp_size:
                alert(1)
                print 'USED RESTORE POINT STORAGE SPACE '+ str(USED) + str(ST.split(' ')[1])+ ' IS GREATER THAN  THRESHOLD SPACE'
                print 'For more  details:'
                v1=os.popen('vssadmin list shadowstorage /for=%s '%drive).read()
                info1=re.findall('(For\svolume|Shadow\sCopy\sStorage\svolume):(.*)',v1)
                for i in range(0,len(info1)):
                    print''.join(info1[i]).replace('\\\\?\\','  ').strip('\\')
                print '\n'
##              date and info
                fin=ecmd('vssadmin list shadows /for=%s ' %drive)
                fin_list=list(fin)
                for g in range(0,len(fin_list)-1):
                    print fin_list[g]   
            else:
                print 'USED RESTORE POINT STORAGE SPACE '+ str(USED) + str(ST.split(' ')[1])+' IS LESS THAN THRESHOLD SPACE'
                alert(0)
