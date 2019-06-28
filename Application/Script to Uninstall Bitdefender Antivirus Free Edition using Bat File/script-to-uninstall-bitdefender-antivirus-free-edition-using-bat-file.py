BAT=r'''
@echo off
rmdir "C:\Program Files\Bitdefender Antivirus Free\bdagent.exe" /s /q
reg delete "HKEY_CURRENT_USER\SOFTWARE\Bitdefender\Bitdefender Antivirus Free" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Bitdefender\Bitdefender Antivirus Free" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{1FCCF41D-5F00-4FE2-9653-162D0486C8B4}" /f
reg delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\updatesrv" /f
reg delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vsserv" /f
rmdir "C:\ProgramData\Bitdefender\Bitdefender Antivirus Free" /s /q
rmdir "C:\Program Files\Bitdefender Antivirus Free" /s /q
rmdir "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Bitdefender Antivirus Free" /s /q
del "C:\Users\Public\Desktop\Bitdefender Antivirus Free.Ink" /s /q
'''
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
	print "Bitdefender antivirus free edition uninstall sucessfully"
	print stdout

if os.path.exists(path):
	try:
		os.remove(path)
	except:
		pass
