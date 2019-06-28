import _winreg
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
with disable_file_system_redirection():
    cmd=os.popen("wmic product get name").read()
if "Java" in cmd:
    if os.path.exists(r"C:\Program Files (x86)"):
        handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Wow6432Node\JavaSoft\Java Update\Policy",0,_winreg.KEY_ALL_ACCESS);
        _winreg.SetValueEx(handle, 'EnableJavaUpdate', 0,_winreg.REG_DWORD, 0)
        _winreg.SetValueEx(handle, 'NotifyDownload', 0,_winreg.REG_DWORD, 0)
        handle.Close()
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run",0,_winreg.KEY_ALL_ACCESS);
        try:
            _winreg.DeleteValue(key, "SunJavaUpdateSched")
        except Exception as e:
            print e
        key.Close()
        print "Java Updater Disabled....:-)"
    else:
        handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\JavaSoft\Java Update\Policy",0,_winreg.KEY_ALL_ACCESS);
        _winreg.SetValueEx(handle, 'EnableJavaUpdate', 0,_winreg.REG_DWORD, 0)
        _winreg.SetValueEx(handle, 'NotifyDownload', 0,_winreg.REG_DWORD, 0)
        handle.Close()
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",0,_winreg.KEY_ALL_ACCESS);
        try:
            _winreg.DeleteValue(key, "SunJavaUpdateSched")
        except Exception as e:
            print e
        key.Close()
        print "Java Updater Disabled....:-)"

else:
    print "Java software not installed at endpoint :-("



