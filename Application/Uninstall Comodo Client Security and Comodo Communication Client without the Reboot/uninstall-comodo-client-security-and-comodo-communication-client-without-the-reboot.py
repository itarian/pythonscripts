import os
import ctypes
import re
import time
import _winreg
from _winreg import *
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
def check():
    
    with disable_file_system_redirection():
        inst=os.popen("wmic product get name,identifyingnumber").read()
         
        
    return inst
unins=["COMODO Client - Security", "COMODO Client - Communication Updater", "COMODO Client - Communication"]
def reg(i):

    blacklist=i
    def collectprograms(rtkey,pK,kA):
        try:
            list=[]
            oK=_winreg.OpenKey(rtkey,pK,0,kA)
            i=0
            while True:
                try:
                    bkey=_winreg.EnumKey(oK,i)
                    vkey=os.path.join(pK,bkey)
                    oK1=_winreg.OpenKey(rtkey,vkey,0,kA)
                    try:
                        DN,bla=_winreg.QueryValueEx(oK1,'DisplayName')
                        inlist=[DN.strip(), vkey, pK]
                        list.append(inlist)
                        
                    except:
                        pass
                    i+=1
                except:
                    break
        except:
            pass
        return list

        
    uninstallkey_32='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'

    if 'PROGRAMFILES(X86)' in os.environ.keys():
        
        rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey_32,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
                (_winreg.HKEY_LOCAL_MACHINE,uninstallkey_32,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey_32,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey_32,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ)]
    else:
        
        rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey_32,_winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey_32,_winreg.KEY_READ)]

    bet=[]
    for i in rklist:
        col=collectprograms(i[0], i[1], i[2])
        for c in col:
            
            if blacklist in c:
                bet.append(c[1])

    if not bet:
        print "Please blacklist Valid Installed Software"
    else:
        for i in bet:
            
            j=i.replace(" ", '" "')
            v='\\'
            path="HKEY_LOCAL_MACHINE"+v+i
            path1="HKEY_LOCAL_MACHINE"+v+j
            got=path1
            
            
    return got
            

def uninstall (find):
	command="MsiExec.exe /X"+find+" /qn CESMCONTEXT=1 REBOOT=REALLYSUPPRESS"
	uninst=os.popen(command).read()
	time.sleep(120)
	inst=check()



inst=check()
 
if len(inst)>0:
    for i in unins:
        if "Security" in i:
            find=re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity',inst)
            if len(find)<=0:
                print "Comodo Client Security is not uninstalled on Endpoint"
                print "Please restart the computer and Try again"
        elif "Updater" in i:
            find=re.findall('{.*}\s\sCOMODO\sClient\s-\sCommunication\sUpdater',inst)
            if len(find)<=0:
                print "COMODO Client - Communication Updater is not uninstalled on Endpoint"
        else:
            find=re.findall('{.*}\s\sCOMODO\sClient\s-\sCommunication',inst)
            if len(find)<=0:
                print "COMODO Client - Communication is not uninstalled on Endpoint"
		
        if len(find)>0:
            final=re.findall('{.*}',find[0])[0]
            if len(final) != 39:
                fin=reg(i)
                fina=fin.split('\\')[-1]
                final1=re.findall('{.*}',fina)[0]
                print i+" is installed on Endpoint"
                print "GUID from Registry is : "+final1
                print "Uninstalling has started ..."
                uninstall(final1)
                
                  

                
            elif len(final) == 39:
                print i+" is installed on Endpoint"
                print "GUID from command prompt is :"+final
                print "Uninstalling has started ..."
                uninstall(final)
        print "Comodo product's uninstalled from the endpoint"  

             
       
           
