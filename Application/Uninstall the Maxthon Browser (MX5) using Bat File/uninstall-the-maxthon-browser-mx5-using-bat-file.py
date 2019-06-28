BAT=r'''
@echo off
SC DELETE MxService

reg delete "HKEY_CURRENT_USER\SOFTWARE\Maxthon5" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Applications\Maxthon.exe" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Applications\Maxthon.exe\shell\open\command" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Maxthon5" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Maxthon5" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\RegisteredApplications" /f
reg delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MxService" /f
reg delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\FirewallRules" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\MaxthonAddonFile" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Clients\StartMenuInternet\Maxthon5" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\MaxthonRssFile" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\MaxthonSkinFile" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\MaxthonUrlFile" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\MaxthonRadioFile" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\MaxthonPdfFile" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\MaxthonImageFile" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\MaxthonDictionaryFile" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Maxthon5" /f

rmdir "C:\Program Files (x86)\Maxthon5" /s /q
rmdir "C:\Program Files\Maxthon5" /s /q
rmdir "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\MX5" /s /q
rmdir "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\MX5\Uninstall.Ink" /s /q
rmdir "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\MX5\Visit Maxthon Forum.url" /s /q
del "C:\Users\%username%\AppData\Local\Temp\MxUninstall" /s /q
del "C:\Users\%username%\AppData\Roaming\Maxthon5" /s /q
del "C:\Windows\System32\Tasks\Maxthon5 Update" /s /q

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
with open(path,"w") as f:
    f.write(BAT)
    
with disable_file_system_redirection():
	print "Excuting Bat File"
	process = subprocess.Popen([path],stdout=subprocess.PIPE)
	stdout = process.communicate()[0]
	print "mx5 uninstall sucessfully"
	print stdout

if os.path.exists(path):
	try:
		os.remove(path)
	except:
		pass

