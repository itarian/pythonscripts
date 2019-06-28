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
        reg_cmd2=os.popen('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\CloudContent" /v "DisableWindowsConsumerFeatures" /t "REG_DWORD" /d "1" /f').read()
        reg_cmd4=os.popen('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsStore" /v "AutoDownload" /t "REG_DWORD" /d "2" /f').read()
        print 'Registry Settings are updated'
    except Exception as err:
        print "Updated failed due to the below error"
        print err


import os
d=os.popen('systeminfo | findstr /B /C:"OS Name"').read()
if "10" in d:
    if "Enterprise" in d:
        try:
            print'Disabling the Windows 10 "Get Updates" Pop-up files'
            Registry_Edit()
            print 'Please restart the endpoint to apply changes ....'
        except Exception as err:
            print "Operation failed due to the below error"
            print err
    elif "Education" in d:
        try:
            print'Disabling the Windows 10 "Get Updates" Pop-up files'
            Registry_Edit()
            print 'Please restart the endpoint to apply changes ....'
        except Exception as err:
            print "Operation failed due to the below error"
            print err
    else:
         print "INFO - This Disabling feature is only applicable to windows 10 Enterprise and Education Versions....."
else:
    print "INFO - This Disabling feature is only applicable to windows 10 Enterprise and Education Versions....."


