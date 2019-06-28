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
            
with disable_file_system_redirection():
    import _winreg;
    key = getattr(_winreg,"HKEY_LOCAL_MACHINE")
    subkey = _winreg.OpenKey(key, "Software\Microsoft\Windows\CurrentVersion\Policies\System" )
    (value, type) = _winreg.QueryValueEx(subkey,"EnableLUA")
    if value == 1:
       print("User Access Control is Enabled");
    elif value == 0:
       print("User Access Control is Disabled");
    else:
       print('Error code returned');
