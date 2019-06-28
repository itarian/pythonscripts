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

def turnoff_capslock():
    dll = ctypes.WinDLL('User32.dll')
    VK_CAPITAL = (0X14)
    if dll.GetKeyState(VK_CAPITAL):
        print"Caps Lock is turned OFF"
        dll.keybd_event(VK_CAPITAL, 0X3a, 0X1, 0)
        dll.keybd_event(VK_CAPITAL, 0X3a, 0X3, 0)    
        print dll.GetKeyState(VK_CAPITAL)
    else:
        print "Caps Lock is already in OFF state"

turnoff_capslock()
