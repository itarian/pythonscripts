import subprocess
import ctypes
import _winreg
import sys
import os
import re
import os,re,sys
import _winreg,difflib,filecmp
import time

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)



final_check=0

try:
    
    if 'PROGRAMFILES(X86)' in os.environ.keys():
        handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\WOW6432Node\COMODO\Dome Agent\config",0,_winreg.KEY_ALL_ACCESS)
        _winreg.DeleteValue(handle, 'pwd-hash')
        
        
    else:
        handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\COMODO\Dome Agent\config",0,_winreg.KEY_ALL_ACCESS)
        _winreg.DeleteValue(handle, "pwd-hash")
        

except:
    final_check=final_check+1
    
def uninstall():
        ch=[];
        with disable_file_system_redirection():
            guid=os.popen('powershell.exe "get-wmiobject Win32_Product | Format-Table Name,IdentifyingNumber" |  findstr /i /c:"Comodo Dome Agent" ').read();
        ch.append(re.findall("{.*",guid));
        dome=[];
        for i in ch[0]:
            dome.append(i)

        li=[]
        def collectprograms(rtkey,pK,kA):
            import _winreg
            import os
            try:      
                oK=_winreg.OpenKey(rtkey,pK,0,kA)
                
                i=0
                while True:
                  try:
                   bkey=_winreg.EnumKey(oK,i)
                   vkey=os.path.join(pK,bkey)
                   oK1=_winreg.OpenKey(rtkey,vkey,0,kA)
                   
                   try:
                       DN,bla=_winreg.QueryValueEx(oK1,'DisplayName')
                       DV,bla=_winreg.QueryValueEx(oK1,'QuietUninstallString')
                       DV1,bla=_winreg.QueryValueEx(oK1,'UninstallString')
                       li.append([DN.strip(),DV.strip(),DV1.strip()])
                   except:
                    pass
                   i+=1
                  except:
                   break
            except:
                pass
            
            _winreg.CloseKey(oK)
            return li

        def programsinstalled():
         uninstallkey='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
         if 'PROGRAMFILES(X86)' in os.environ.keys():
          rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
              (_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ),
              (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
              (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ)]
          
         else:
          rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_READ),
              (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_READ)]
          
         for i in rklist:
             col=collectprograms(i[0], i[1], i[2])
             return col
        k=programsinstalled()
        for i in k:
            if 'Comodo Dome Agent' in i[0]:
                print i[0]+" uninstallition has started"
                
                u1=i[1]
                with disable_file_system_redirection():
                    CMD='%s'%u1
                    try:
                        process=subprocess.Popen(CMD,shell=True,stdout=subprocess.PIPE)
                        result=process.communicate()
                        ret=process.returncode
                    
                    except:
                        pass
                    
                
                
                u2=i[2]
                with disable_file_system_redirection():
                    CMD1='%s /quiet'%u2
                    try:
                        process=subprocess.Popen(CMD1,shell=True,stdout=subprocess.PIPE)
                        result=process.communicate()
                        ret=process.returncode
                    
                    except:
                        pass
            
            
        if dome:
            with disable_file_system_redirection():
                process=subprocess.Popen(['MsiExec.exe','/x',dome,'/q'],shell=True,stdout=subprocess.PIPE)
                result=process.communicate()
                ret=process.returncode
        else:
            pass
        
def check():
    check=os.popen("wmic product get name").read()

    if "Comodo Dome Agent" in check:
        print "Comodo Dome Agent is not uninstalled"

    else:
        print "Comodo Dome Agent removed successfully"


if final_check >0:
    print "Comodo Dome Agent is not installed in endpoint"

else:
    uninstall()
    time.sleep(60)
    check()


