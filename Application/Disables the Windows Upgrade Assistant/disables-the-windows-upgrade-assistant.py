#COPY YOUR BAT FILE CONETENT TO RUN BATCH FILE 

BAT=r'''
@echo off

REM Stop Update Assistant if running
taskkill -f -im UpdateAssistant.exe
taskkill -f -im UpdateAssistantCheck.exe
taskkill -f -im Windows10Upgrade.exe
taskkill -f -im Windows10UpgraderApp.exe

REM Block Update Assistant with Windows Firewall
netsh advfirewall firewall delete rule name="Windows 10 Update Assistant" dir=in
netsh advfirewall firewall delete rule name="Windows 10 Update Assistant" dir=out
netsh advfirewall firewall add rule name="Windows 10 Update Assistant" dir=in action=block program="C:\Windows\UpdateAssistant\UpdateAssistant.exe" enable=yes
netsh advfirewall firewall add rule name="Windows 10 Update Assistant" dir=out action=block program="C:\Windows\UpdateAssistant\UpdateAssistant.exe" enable=yes
netsh advfirewall firewall add rule name="Windows 10 Update Assistant" dir=in action=block program="C:\Windows\UpdateAssistant\UpdateAssistantCheck.exe" enable=yes
netsh advfirewall firewall add rule name="Windows 10 Update Assistant" dir=out action=block program="C:\Windows\UpdateAssistant\UpdateAssistantCheck.exe" enable=yes
netsh advfirewall firewall add rule name="Windows 10 Update Assistant" dir=in action=block program="C:\Windows\UpdateAssistant\Windows10Upgrade.exe" enable=yes
netsh advfirewall firewall add rule name="Windows 10 Update Assistant" dir=out action=block program="C:\Windows\UpdateAssistant\Windows10Upgrade.exe" enable=yes
netsh advfirewall firewall add rule name="Windows 10 Update Assistant" dir=in action=block program="C:\Windows\UpdateAssistantV2\Windows10Upgrade.exe" enable=yes
netsh advfirewall firewall add rule name="Windows 10 Update Assistant" dir=out action=block program="C:\Windows\UpdateAssistantV2\Windows10Upgrade.exe" enable=yes
netsh advfirewall firewall add rule name="Windows 10 Update Assistant" dir=in action=block program="C:\Windows10Upgrade\Windows10UpgraderApp.exe" enable=yes
netsh advfirewall firewall add rule name="Windows 10 Update Assistant" dir=out action=block program="C:\Windows10Upgrade\Windows10UpgraderApp.exe" enable=yes

REM Disable Update Assistant Scheduled Tasks
c:\windows\system32\schtasks.exe /change /tn "Microsoft\Windows\UpdateOrchestrator\UpdateAssistant" /DISABLE
c:\windows\system32\schtasks.exe /change /tn "Microsoft\Windows\UpdateOrchestrator\UpdateAssistantAllUsersRun" /DISABLE
c:\windows\system32\schtasks.exe /change /tn "Microsoft\Windows\UpdateOrchestrator\UpdateAssistantCalendarRun" /DISABLE
c:\windows\system32\schtasks.exe /change /tn "Microsoft\Windows\UpdateOrchestrator\UpdateAssistantWakeupRun" /DISABLE

exit
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
	print "---------------------------"
	print stdout

if os.path.exists(path):
	try:
		os.remove(path)
	except:
		pass
