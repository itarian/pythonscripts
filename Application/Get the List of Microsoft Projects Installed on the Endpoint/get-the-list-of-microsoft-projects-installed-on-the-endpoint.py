#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name
import os
import platform
import _winreg,getpass

def gid():
    winreg = _winreg
    REG_PATH1 = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    REG_PATH2 = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    registry_key = winreg.OpenKey( winreg.HKEY_LOCAL_MACHINE, REG_PATH1, 0, winreg.KEY_READ)
    winreg.CloseKey(registry_key)
    name = []
    string=[]
    try:
        registry_key = winreg.OpenKey( winreg.HKEY_LOCAL_MACHINE, REG_PATH1, 0, winreg.KEY_READ)
        i=0

        while True:
            try:
                sub_registry_key = winreg.EnumKey(registry_key, i)
                newpath1 = REG_PATH1 + '\\' + sub_registry_key
                new_registry_key = winreg.OpenKey( winreg.HKEY_LOCAL_MACHINE, newpath1, 0, winreg.KEY_READ)
                try:
                    DisplayName, getname = winreg.QueryValueEx(new_registry_key, 'DisplayName')
                    UninstallString, getname = winreg.QueryValueEx(new_registry_key, 'UninstallString')
                    winreg.CloseKey(new_registry_key)
                    name.append(DisplayName)
                    string.append( UninstallString )
                except:
                    pass
                i += 1
            except:
                break
    except:
        pass
    try:
        registry_key1 = winreg.OpenKey( winreg.HKEY_LOCAL_MACHINE, REG_PATH2, 0, winreg.KEY_READ)
        ii=0
        while True:
            try:
                sub_registry_key1 = winreg.EnumKey(registry_key1, ii)
                newpath2 = REG_PATH2 + '\\' + sub_registry_key1
                new_registry_key1 = winreg.OpenKey( winreg.HKEY_LOCAL_MACHINE, newpath2, 0, winreg.KEY_READ)
                try:
                    DisplayName1, getname = winreg.QueryValueEx(new_registry_key1, 'DisplayName')
                    DisplayVersion1, getname = winreg.QueryValueEx(new_registry_key1, 'DisplayVersion')
                    UninstallString1, getname = winreg.QueryValueEx(new_registry_key1, 'UninstallString')
                    winreg.CloseKey(new_registry_key1)
                    name.append(DisplayName1)
                    string.append(UninstallString1 )
                except:
                    pass
                ii += 1
            except:
                break
    except:
        pass
    try:
        registry_key2 = winreg.OpenKey( winreg.HKEY_CURRENT_USER, REG_PATH1, 0, winreg.KEY_READ)
        iii=0
        while True:
            try:
                sub_registry_key2 = winreg.EnumKey(registry_key2, iii)
                newpath3 = REG_PATH1 + '\\' + sub_registry_key2
                new_registry_key2 = winreg.OpenKey( winreg.HKEY_CURRENT_USER, newpath3, 0, winreg.KEY_READ)
                try:
                    DisplayName2, getname = winreg.QueryValueEx(new_registry_key2, 'DisplayName')
                    UninstallString2, getname = winreg.QueryValueEx(new_registry_key2, 'UninstallString')
                    winreg.CloseKey(new_registry_key2)
                    name.append( DisplayName2)
                    string.append(UninstallString2 )
                except:
                    pass
                iii += 1
            except:
                break
    except:
        pass
    try:
        registry_key3 = winreg.OpenKey( winreg.HKEY_CURRENT_USER, REG_PATH2, 0, winreg.KEY_READ)
        iiii=0
        while True:
            try:
                sub_registry_key3 = winreg.EnumKey(registry_key3, iiii)
                newpath4 = REG_PATH2 + '\\' + sub_registry_key3
                new_registry_key3 = winreg.OpenKey( winreg.HKEY_CURRENT_USER, newpath4, 0, winreg.KEY_READ)
                try:
                    DisplayName3, getname = winreg.QueryValueEx(new_registry_key3, 'DisplayName')
                    UninstallString3, getname = winreg.QueryValueEx(new_registry_key3, 'UninstallString')
                    winreg.CloseKey(new_registry_key3)
                    name.append( DisplayName3 )
                    string.append(UninstallString3 )
                except:
                    pass
                iiii += 1
            except:
                break
    except:
        pass
    out={}
    c=0
    found=[]
    for i in name:
        if i.startswith('Microsoft Project Professional'):
            found.append(i)
    
    if len(found)!=0:
        print 'The software'+i +' is present in  your system'            
    else:
        print 'There is no software,like Microsoft Project Professional/plus is present in  your system'
        
gid()
