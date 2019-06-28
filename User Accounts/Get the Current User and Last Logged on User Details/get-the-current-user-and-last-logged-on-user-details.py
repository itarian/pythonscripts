import os
import ctypes
import subprocess
import re
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
with disable_file_system_redirection():
    current_user = os.popen('query user').read()
    user_details = os.popen("WMIC PATH Win32_NetworkLoginProfile GET   LastLogon,Name").read()
    if current_user == "":
        print "Current User : No user has logged in"
        print "                                               "
        print "The Last logged on details"
        for i in [i.strip() for i in user_details.split('\n') if 'NT AUTHORITY' not in i if i.strip()]:
            print i
    else:
        print "The Current user details"
        print current_user
        print "                                               "
        print "The Last logged on details"
        for i in [i.strip() for i in user_details.split('\n') if 'NT AUTHORITY' not in i if i.strip()]:
            print i
