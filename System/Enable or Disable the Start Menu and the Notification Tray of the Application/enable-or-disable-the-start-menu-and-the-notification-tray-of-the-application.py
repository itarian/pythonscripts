option='3'
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


def disable_startup():
    cmd="reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v NoStartMenuMorePrograms /t REG_DWORD /d 1 /f"
    cmd1="reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v NoStartMenuMFUProgramsList /t REG_DWORD /d 1 /f"
    print 'Removing content from start menu '
    with disable_file_system_redirection():
        disable_startmenu = os.popen(cmd).read()
        disable_startmenu = os.popen(cmd1).read()
        print disable_startmenu
        print 'Done..'

def disable_notifarea():
    cmd= "reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v NoTrayItemsDisplay /t REG_DWORD /d 1 /f"
    cmd1="reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v HideClock /t REG_DWORD /d 1 /f "
    print "Disabling access to notification area "
    with disable_file_system_redirection():
        disable_notif = os.popen(cmd).read()
        disable_clock = os.popen(cmd1).read()
        print disable_notif
        print disable_clock
        print 'Done..'
        
def enable_startup():
    cmd="reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v NoStartMenuMorePrograms /t REG_DWORD /d 0 /f"
    cmd1="reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v NoStartMenuMFUProgramsList /t REG_DWORD /d 1 /f"
    print "Enabling startup"
    with disable_file_system_redirection():
        enable_startmenu = os.popen(cmd).read()
        enable_startmenu = os.popen(cmd1).read()
        print enable_startmenu
        print 'Done..'

def enable_notifarea():
    cmd= "reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v NoTrayItemsDisplay /t REG_DWORD /d 0 /f"
    cmd1="reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v HideClock /t REG_DWORD /d 0 /f "
    print "Enabling access to notification area "
    with disable_file_system_redirection():
        enable_notif = os.popen(cmd).read()
        enable_clock=os.popen(cmd1).read()
        print enable_notif
        print enable_clock
        print 'Done..'

a=os.popen('shutdown -r').read()
print 'Restarting at the endpoint to applying the changes'
print a

if option == '1':
    disable_startup()

elif option == '2':
    disable_notifarea()

elif option == '3':
    enable_startup()

elif option == '4':
    enable_notifarea()
    
    

    
    

    
    
    
    
    
