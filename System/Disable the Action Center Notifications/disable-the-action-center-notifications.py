import os
import platform
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

os_details = platform.release()
print os_details


if "7" in os_details:
    cmd1= "REG ADD HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer  /v HIDESCAHEALTH /t REG_DWORD /d 1 /f"
    print 'Disabling Action center notification begins....'
    with disable_file_system_redirection():
		disable_ac_1 = os.popen(cmd1).read()
		print disable_ac_1
		print 'Done..'
	
else:
    cmd2= "REG ADD HKLM\Software\Policies\Microsoft\Windows\Explorer /v DisableNotificationCenter /t REG_DWORD /d 1 /f"
    print 'Disabling Action center notification begins....'
    with disable_file_system_redirection():
        disable_ac_2 = os.popen(cmd2).read()
        print disable_ac_2
    print 'Done..'
	
print 'Restarting the endpoint to apply changes ....'
val=os.popen('shutdown -r').read()


