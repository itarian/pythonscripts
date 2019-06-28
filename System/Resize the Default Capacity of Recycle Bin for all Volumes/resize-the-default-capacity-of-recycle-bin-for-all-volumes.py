X=1 #please provide the value for increase or decrease the recycle bin capacity size.
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
    def modRecycle(P_AGE):
        import _winreg
        import os
        subkey = r'Software\Microsoft\Windows\CurrentVersion\Explorer\BitBucket\Volume'
        subkeys = []
        with _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, subkey, 0, _winreg.KEY_ALL_ACCESS) as key:
            i = 0
            while i >= 0:
                try:
                    vskey = _winreg.EnumKey(key, i)
                    subkeys.append(os.path.join(subkey, vskey))
                    i += 1
                except:
                    i = -1
        C = 0
        for k in subkeys:
            print 'Volume {}:'.format(C)
            with _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, k, 0, _winreg.KEY_ALL_ACCESS) as key:
                MB, T = _winreg.QueryValueEx(key, 'MaxCapacity')
                _winreg.SetValueEx(key, 'MaxCapacity', 0, _winreg.REG_DWORD, int(MB+MB*(P_AGE/100.0)))
                print 'Old Capacity: {} MB'.format(MB)
                UMB, UT = _winreg.QueryValueEx(key, 'MaxCapacity')
                if MB != UMB:
                    print 'New Capacity: {} MB'.format(UMB)
                else:
                    print 'Sorry, Your Volume {} has no suffient freespace!'.format(C)
                if len(subkeys)-1 != C:
                    print '\n'
            C += 1

    def main(P_AGE):        
        INCHA = '='
        INCHA = INCHA*7
        if P_AGE > 0:
            print '{} Increased by {}% {}'.format(INCHA, P_AGE, INCHA)
            modRecycle(P_AGE)
        elif P_AGE < 0:
            print '{} Decreased by {}% {}'.format(INCHA, P_AGE*(-1), INCHA)
            modRecycle(P_AGE)
        else:
            print 'Sorry, There is no effect since you have given 0 for P_AGE variable'

    if __name__ == '__main__':
        main(X) ##User can the value here to increase or decrease the Re-Cycle Bin capacity of default size.
    ##For example, -10 for decreasing 10% from Default size
    ##For example, 10 for increasing 10% to Default size
