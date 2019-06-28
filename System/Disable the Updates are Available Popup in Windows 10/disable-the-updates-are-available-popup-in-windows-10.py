import os
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


def Registry_Edit():
    import os 
    try:      
        reg_cmd1=os.popen('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v "AUOptions" /t "REG_DWORD" /d "4" /f').read()
        reg_cmd2=os.popen('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v "NoAutoUpdate" /t "REG_DWORD" /d "0" /f').read()
        reg_cmd3=os.popen('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v "ScheduledInstallDay" /t "REG_DWORD" /d "1" /f').read()
        reg_cmd4=os.popen('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v "ScheduledInstallFourthWeek" /t "REG_DWORD" /d "1" /f').read()
        reg_cmd5=os.popen('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v "ScheduledInstallTime" /t "REG_DWORD" /d "3" /f').read()
        reg_cmd6=os.popen('reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\MusNotification.exe" /v "debugger" /d "rundll32.exe" /f').read()
        reg_cmd7=os.popen('reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\MusNotificationUx.exe" /v "debugger" /d "rundll32.exe" /f').read()
        print  "Registry settings are successfully updated"
    except Exception as err:
        print "Updated failed due to the below error"
        print err


import os
d=os.popen('systeminfo | findstr /B /C:"OS Name"').read()
if "10" in d:
    try:
        print'Disabling the Windows 10 "Get Updates" Pop-up files'
        disable_file_system_redirection().__enter__()
        import os
        print os.popen('takeown /f C:\\Windows\\System32\\MusNotification.exe').read()
        print os.popen('icacls C:\\Windows\\System32\\MusNotification.exe /deny Everyone:(X)').read()
        print os.popen('icacls C:\\Windows\\System32\\MusNotification.exe /deny Administrators:(X)').read()
        print os.popen('icacls C:\\Windows\\System32\\MusNotification.exe /deny Users:(X)').read()
        print os.popen('icacls C:\\Windows\\System32\\MusNotification.exe /deny "ALL APPLICATION PACKAGES":(X)').read()
        print os.popen('takeown /f C:\\Windows\\System32\\MusNotificationUx.exe').read()
        print os.popen('icacls C:\\Windows\\System32\\MusNotificationUx.exe /deny Everyone:(X)').read()
        print os.popen('icacls C:\\Windows\\System32\\MusNotificationUx.exe /deny Administrators:(X)').read()
        print os.popen('icacls C:\\Windows\\System32\\MusNotificationUx.exe /deny Users:(X)').read()
        print os.popen('icacls C:\\Windows\\System32\\MusNotificationUx.exe /deny "ALL APPLICATION PACKAGES":(X)').read()
        print 'Command operations are executed'
        Registry_Edit()
        h=os.popen('gpupdate').read()
        print '                                           '
        print 'Please restart the endpoint to apply changes ....'
    except Exception as err:
        print "Operation failed due to the below error"
        print err
else:
     print "INFO - This popup notification is only applicable to windows 10 machines....."


