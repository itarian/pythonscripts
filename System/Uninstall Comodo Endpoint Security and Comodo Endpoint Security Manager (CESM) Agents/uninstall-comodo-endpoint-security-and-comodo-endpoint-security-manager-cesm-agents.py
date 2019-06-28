import os
import ctypes
from subprocess import PIPE, Popen
import time
import re
#import _winreg
try:
    import winreg as _winreg
except ImportError:
    try:
        import _winreg
    except ImportError:
        pass
import getpass
import socket
import os
import shutil
import time
import ssl
import time
import ctypes
try:
    import urllib.request as urllib2
except ImportError:
    try:
        import urllib2
    except ImportError:
        pass
import getpass
ESM = 'COMODO ESM Agent'
CES = 'COMODO Endpoint Security'
CCS = 'COMODO Client - Security'
#Version = "If CES has the name COMODO Client - Security add the version here"
Version = '8.3.0.180204'

class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)

def ecmd(command, output=False):
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
        objt = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
        out, err = objt.communicate()
        ret=objt.returncode
    if not out:
        return ret
    else:
        return '%s\n%s'%(out, err)

def check():        
    return ecmd('wmic product get name,version,IdentifyingNumber| findstr /i /c:"COMODO Endpoint Security" /c:"COMODO ESM Agent" /c:"COMODO Client - Security"| sort')
guid=check()
def uninstall_cesm(find):    
    command=r'MsiExec.exe /X '+find+' /q'
    print (command)
    cesm=ecmd(command, True)
    print (cesm)
    time.sleep(90)
    inst=check()
    if inst:
        find=re.findall('{.*}\s\sCOMODO\sESM\sAgent',inst)
        if len(find) >0:        
            print ("Comodo ESM Agent is not uninstalled on Endpoint")
            print ("Please restart the computer and Try again")
            return(1)
    else :
        print ("Uninstallation is Successful")		
        return(0)
    
        

def uninstall_ces(find):    
    flag=r'reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\COMODO\CIS\ESM" /f'
    print (ecmd(flag,True))
    command=r'MsiExec.exe /X '+find+' /quiet REBOOT=ReallySuppress REMOVE=ALL'
    print (command)
    ces=ecmd(command, True)
    time.sleep(90)
    inst=check()
    if inst:
        find=re.findall('{.*}\s\sCOMODO\sEndpoint\sSecurity',inst)
        if len(find) >0:        
            print ("Comodo Endpoint Security is not uninstalled on Endpoint")
            print ("Please restart the computer and Try again")
            WrireRegcreate()
            print('reg key created created')
            writescript()
            print('script screated')
            print ('System will restart in 5 minutes')
            print (ecmd(r'shutdown.exe -r -t 300 /f ', True))
            return(1)
    else :
        print ("Uninstallation is Successful")
        return(0)

def uninstall_ces2(find):    
    flag=r'reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\COMODO\CIS\ESM" /f'
    print (ecmd(flag,True))
    command=r'MsiExec.exe /X '+find+' /quiet REBOOT=ReallySuppress REMOVE=ALL'
    print (command)
    ces=ecmd(command, True)
    time.sleep(90)
    inst=check()
    if inst:
        find=re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity ',inst)
        if len(find) >0:        
            print ("Comodo Client - Security is not uninstalled on Endpoint")
            print ("Please restart the computer and Try again")
            WrireRegcreate()
            print('reg key created created')
            writescript()
            print('script screated')
            print ('System will restart in 5 minutes')
            print (ecmd(r'shutdown.exe -r -t 300 /f ', True))
            return(1)
    else :
        print ("Uninstallation is Successful")
        return(0)

def WrireRegcreate():
    try:
        keyval="SYSTEM\\comodoinstall"
        try:
            reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
            ok = _winreg.OpenKey(reg,keyval,0,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
            _winreg.CloseKey(ok)
            print("key present")
        except:
            print("key not found")
            key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,keyval)
            print("key created")
            _winreg.CloseKey(key)
        return True
    except WindowsError:
        return False

def WrireRegdelete():
    try:
        keyval="SYSTEM\\comodoinstall"
        try:
            reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
            ok = _winreg.OpenKey(reg,keyval,0,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
            _winreg.CloseKey(ok)
            print("key present next delete key")
            key = _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE,keyval)
            print("delete key")
            _winreg.CloseKey(key)
        except:
            print("key not found")
        return True
    except WindowsError:
        return False

def writescript():
    f1 = open(os.path.expandvars("%SystemDrive%\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\test.vbs"), "w")
    f1.write('Set objFSO = CreateObject("Scripting.FileSystemObject")\r\n')
    f1.write('Const HKEY_LOCAL_MACHINE = &H80000002\r\n') 
    f1.write('strComputer = "."\r\n')
    f1.write('strKeyPath = "SYSTEM\\comodoinstall"\r\n')
    f1.write('Set objRegistry = GetObject("winmgmts:\\\\" & strComputer & "\\root\default:StdRegProv")\r\n')
    f1.write('DeleteSubkeys HKEY_LOCAL_MACHINE, strKeypath\r\n')
    f1.write('Sub DeleteSubkeys(HKEY_LOCAL_MACHINE, strKeyPath)\r\n')
    f1.write('    objRegistry.EnumKey HKEY_LOCAL_MACHINE, strKeyPath, arrSubkeys\r\n')
    f1.write('    If IsArray(arrSubkeys) Then\r\n')
    f1.write('        For Each strSubkey In arrSubkeys\r\n')
    f1.write('            DeleteSubkeys HKEY_LOCAL_MACHINE, strKeyPath & "\\" & strSubkey\r\n')
    f1.write('        Next\r\n')
    f1.write('    End If\r\n')
    f1.write('    objRegistry.DeleteKey HKEY_LOCAL_MACHINE, strKeyPath\r\n')
    f1.write('End Sub\r\n')
    f1.write('strScript = Wscript.ScriptFullName\r\n')
    f1.write('objFSO.DeleteFile(strScript)\r\n')
    f1.close

def uninstallesmces():
    inst=check()
    print (inst)

    if len(inst)>0:
        find=re.findall('{.*}\s\sCOMODO\sESM\sAgent ',inst)
        if len(find)>0:
                final=re.findall('{.*}',find[0])[0]            
                if len(final) >0:
                        print ("COMODO ESM Agent  is installed on Endpoint")
                        print ("Uninstalling has started ")
                        result1=uninstall_cesm(final)
        else:
            result1=-1

    if len(inst)>0:
        find=re.findall('{.*}\s\sCOMODO\sEndpoint\sSecurity ',inst)
        if len(find)>0:
                final=re.findall('{.*}',find[0])[0]
                if len(final) >0:
                        print ("C0OMODO Endpoint Security  is installed on Endpoint")
                        print ("Uninstalling has started ")
                        result2=uninstall_ces(final)
        else:
            result2=-1

    print (result1,result2)

    if (result2==0):
        WrireRegcreate()
        print('reg key created created')
        writescript()
        print('script screated')
        print ('System will restart in 5 minutes')
        print (ecmd(r'shutdown.exe -r -t 300 /f', True))
   
    elif result1==-1 or result2==-1:     
        print ("ESM Agent and CES not detected")

def uninstallesmces2():
    inst=check()
    print (inst)

    if len(inst)>0:
        find=re.findall('{.*}\s\sCOMODO\sESM\sAgent ',inst)
        if len(find)>0:
                final=re.findall('{.*}',find[0])[0]            
                if len(final) >0:
                        print ("COMODO ESM Agent  is installed on Endpoint")
                        print ("Uninstalling has started ")
                        result1=uninstall_cesm(final)
        else:
            result1=-1

    if len(inst)>0:
        find=re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity ',inst)
        if len(find)>0:
                final=re.findall('{.*}',find[0])[0]
                if len(final) >0:
                        print ("C0OMODO Client - Security  is installed on Endpoint")
                        print ("Uninstalling has started ")
                        result2=uninstall_ces2(final)
        else:
            result2=-1

    print (result1,result2)

    if (result2==0):
        WrireRegcreate()
        print('reg key created created')
        writescript()
        print('script screated')
        print ('System will restart in 5 minutes')
        print (ecmd(r'shutdown.exe -r -t 300 /f', True))    
    elif result1==-1 and result2==-1:     
        print ("ESM Agent and CES not detected")

def os_platform():
    true_platform = os.environ['PROCESSOR_ARCHITECTURE']
    try:
            true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
    except KeyError:
            pass
            #true_platform not assigned to if this does not exist
    return true_platform


def Wrireferify():
    try:
        keyval="SYSTEM\\comodoinstall"
        reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        ok = _winreg.OpenKey(reg,keyval,0,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
        _winreg.CloseKey(ok)
        print("key present")
        return True
    except WindowsError:
        print("key not found")
        return False


final=os.popen('wmic product get name,version| findstr /i /c:"COMODO Endpoint Security" /c:"COMODO ESM Agent" /c:"COMODO Client - Security"| sort').read()
if (final.find(Version) != -1):
    if ((final.find(ESM) != -1) or (final.find(CES) != -1)):
        print('ESM or CES is present start uninstall cesm and ces')
        uninstallesmces()

    elif ((final.find(CCS) != -1) and (final.find(Version) != -1)):
        print('ESM and CES is NOT present and CCS is present')
        uninstallesmces2()
        if Wrireferify() == True:
            print('CCS and key present request to remove')
            WrireRegdelete()
        else:
            print('CCS is present and the key is not present')
    elif ((final.find(CCS) != -1)):
          if Wrireferify() == True:
            print('CCS and key present request to remove')
            WrireRegdelete()
          else:
              print 'latest version if ccs has been successfully installed'
    else:
        print('ESM and CES is NOT present and CCS is NOT present')   
        
else:
    if ((final.find(ESM) != -1) or (final.find(CES) != -1)):
        print('ESM or CES is present start uninstall cesm and ces')
        uninstallesmces()
    elif ((final.find(CCS) != -1) and (final.find(Version) != -1)):
        print('ESM and CES is NOT present and CCS is present')
        uninstallesmces2()
        if Wrireferify() == True:
            print('CCS and key present request to remove')
            WrireRegdelete()
        else:
          print('CSS is present and the key is not present')

    elif ((final.find(CCS) != -1)):
          if Wrireferify() == True:
            print('CCS and key present request to remove')
            WrireRegdelete()
          else:
              print 'latest version if ccs has been successfully installed'
    else:
        print('ESM and CES is NOT present and CCS is NOT present')
