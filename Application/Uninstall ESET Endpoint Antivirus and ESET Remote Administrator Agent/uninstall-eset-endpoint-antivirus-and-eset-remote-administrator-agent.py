#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name
passwordprotected='0' ## set the value as 1 for password protected in your eset otherwise set the value as 0
password=r'****'  #enter your Eset password
import os
import re
import sys
import getpass
import socket
import time
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

dm,ret2=ecmd('wmic product get name,identifyingnumber| findstr /i "ESET"')
name=os.popen('wmic product get name | findstr /i "ESET"').read()
nm=name.strip().split('\n')
c=0
if ret2!=0:
    print 'ESET products are not installed in your system'
else:    
    v=dm.split('\n')
    fin=[]
    print 'The Following ESET products are installed in your system:\n'
    for i in range(0,len(v)):
        if len(v[i])!=0:
            fin.append(v[i].split(' ')[0])
            print '\t\t\t*)',nm[i]
    if passwordprotected is '1':
        print "\nyou have choose the password protected ESET unnstallation:"
        for k in range(0,len(fin)):
            if len(fin[k])!=0:            
                CMD=('MsiExec.exe /X%s /qb REBOOT="ReallySuppress" PASSWORD="%s"')%(str(fin[k]),str(password))
                ret3=ecmd(CMD)          

    else:
        for k in range(0,len(fin)):
            if len(fin[k])!=0:            
                ret1=ecmd('MsiExec.exe /X%s /qb REBOOT="ReallySuppress"'% fin[k])
                
                
          
    check=ecmd('wmic product get name,identifyingnumber| findstr /i "ESET"')
    if check!=0:
        print '\nESET products are successfully uninstalled in your system'
    else:
        print '\nESET products uninstallation failed'
