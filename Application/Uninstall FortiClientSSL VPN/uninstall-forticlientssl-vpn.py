BAT=r'''
@echo off
net stop FortiSSLVPNdaemon
SC DELETE CacheCleanAP
SC DELETE CacheCleanAP64
SC DELETE FortiSSLVPNdaemon

reg delete "HKEY_CURRENT_USER\Software\Fortinet" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{91C045A0-A2A0-4FBC-9F04-01BD4E090301}" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{B0882EB7-81A5-4A11-8D45-71888F973933}" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{DE64E08D-8F19-4D75-A277-855E9DE74AA5}\InprocServer32" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{DE64E08D-8F19-4D75-A277-855E9DE74AA5}\ProgID" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Forticachecleaner.cachecleaner" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Forticachecleaner.cachecleaner.1" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Forticontrol.fortisslvpn" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Forticontrol.fortisslvpn.1" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{55DACC13-B2A1-4BDC-B069-5F1EDDAEA211}" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{74688165-6022-47DB-8170-A4DBB55AB3D5}" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{8BB244C2-608A-4B48-89EC-2F010AF79556}" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{E3668136-B4B2-4DD6-BFDC-8A0E9DA6DEEF}" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SslvpnHostCheck.FortiHostCheck" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SslvpnHostCheck.FortiHostCheck.1" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\TypeLib\{2897EECE-8996-418B-A0D9-C638FBD221CE}" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\TypeLib\{2FC33C7C-ACAB-4733-8C02-CEE2FF8AFD32}" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\TypeLib\{5F14603F-2FC5-47D5-BDE2-7693DC34E37A}" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\FORTICLIENT" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Components\147BA5BB3192F7B418CA29CAB3852A1C" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Components\32642A6F7834D014B92C68ED55D3C9BB" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Components\4A11D59FA78303740A88AD684E97F4E8" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Components\58F14180363CD5942A3E80DA2EF5C3AB" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Products\08278D9F27933A4408F4429E20C2BA33" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{F9D87280-3972-44A3-804F-24E9022CAB33}" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Fortinet" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\{A34DCE59-0004-0000-2281-3F8A9926B752}" /f


del "‪%systemdrive%\ProgramData\Microsoft\Windows\Start Menu\Programs\FortiClient" /s /q
del "%systemdrive%\Windows\SysWOW64\fortisslclient.key" /s /q
del "%systemdrive%\Windows\SysWOW64\fortisslclient.crt" /s /q
del "%systemdrive%\Windows\SysWOW64\fortisslcacert.pem" /s /q
del "%systemdrive%\Windows\SysWOW64\FortiSSLVPNdaemon.exe" /s /q
del "%systemdrive%\Windows\SysWOW64\fortisslclient.key" /s /q


'''
import os
import sys
import platform
import subprocess
import ctypes
import time
import os
import sys
import platform
import subprocess
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

path=os.environ['programdata']+"\Sample.bat"
def Run():
    
    with open(path,"w") as f:
        f.write(BAT)
    with disable_file_system_redirection():
        process = subprocess.Popen([path],stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
    return path
	
Drive=os.environ['SYSTEMDRIVE']

Path64=Drive+r'\Program Files (x86)\Fortinet'

Path32=Drive+'\Program Files\Fortinet'

if os.path.exists(Path64):
    path=Run()
    try:
        k2=shutil.rmtree(Path64)
    except:
        pass
        
    print "FortiClientSSL VPN is uninstalled successfully"

elif os.path.exists(Path32):
    path=Run()
    try:
        k2=shutil.rmtree(Path32)
    except:
        pass
    print "FortiClientSSL VPN is uninstalled successfully"
else:
    print "FortiClientSSL VPN is not installed in endpoint"

if os.path.exists(path):
    try:
        os.remove(path)
    except:
            pass



