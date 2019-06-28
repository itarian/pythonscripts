import os
import subprocess

unins=["Spiceworks Agent"]
import re
import _winreg
from _winreg import *
blacklist=[]

for i in unins:    
    blacklist.append(i)  
uninstallkey='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
uninstallkey1='SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
if 'PROGRAMFILES(X86)' in os.environ.keys():
    reg_list=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey1,_winreg.KEY_WOW64_32KEY | _winreg.KEY_ALL_ACCESS),
            (_winreg.HKEY_LOCAL_MACHINE,uninstallkey1,_winreg.KEY_WOW64_64KEY | _winreg.KEY_ALL_ACCESS),
            (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_ALL_ACCESS),
            (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_ALL_ACCESS)]
    
else:
    
    reg_list=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_READ,_winreg.KEY_ALL_ACCESS),
            (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_READ,_winreg.KEY_ALL_ACCESS)]
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

final_list=[]
rs = 0
for c in list:
    if c not in final_list:
        final_list.append(c)

for c1 in final_list:
    for i in range(0,len(blacklist)):
        if blacklist[i] == c1[0]:
            Registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            RawKey = _winreg.OpenKey(Registry, c1[1],0,Value)
            (value, type) = _winreg.QueryValueEx(RawKey,"UninstallString")
            strun.append(value)
            Uninstr=re.findall('{.*}',value)
            unin_str=''.join(Uninstr)
            command="msiexec /x "+unin_str+" /qn"
            unarglist= command.splitlines(True)
            unarglist2= ''.join(unarglist)
            
            subprocess.check_call(unarglist2)
            rs += 1
        else:
            rs += 0
if rs:
    print blacklist[i] +' are removed'
    
else:
    print blacklist[i] +' are not available'    
