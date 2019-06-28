
unins=["Cylance PROTECT"]
import os
import re
import subprocess
import _winreg
import _winreg
from _winreg import *
blacklist=[]
for i in unins:    
    blacklist.append(i)  
uninstallkey='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'

if 'PROGRAMFILES(X86)' in os.environ.keys():
    reg_list=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
            (_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ),
            (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
            (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ)]
    
else:
    
    reg_list=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_READ),
            (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_READ)]
strun=[]
list=[]
for i in reg_list:
    reg_key=i[0]
    sub_key=i[1]
    Value=i[2]
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    k = OpenKey(reg, i[1])
    reg =_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, i[1], 0, i[2])
    i=0
    while True:
        try:
            key_value=_winreg.EnumKey(reg,i)
            path=os.path.join(sub_key,key_value)
            Hkey=_winreg.OpenKey(reg_key,path,0,Value)
            try:
                key,dis_name=_winreg.QueryValueEx(Hkey,'DisplayName')
                inlist=[key.strip(), path, sub_key]
                list.append(inlist)
            except:
                pass
            i+=1
        except:
            break
for c in list:
    for i in range(0,len(blacklist)):
        if blacklist[i] in c[0]:
            Registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            RawKey = _winreg.OpenKey(Registry, c[1],0,Value)
            (value, type) = _winreg.QueryValueEx(RawKey,"UninstallString")
            strun.append(value)
            Uninstr=re.findall('{.*}',value)
            unin_str=''.join(Uninstr)
            print unin_str
            command="MsiExec.exe /X"+unin_str+" /qn"
            unarglist2 = command.split()
            try:
                subprocess.check_call(unarglist2)
                print blacklist[i] +'are removed'
            except subprocess.CalledProcessError as e:
                print blacklist[i] +'older Version  does not exist'
