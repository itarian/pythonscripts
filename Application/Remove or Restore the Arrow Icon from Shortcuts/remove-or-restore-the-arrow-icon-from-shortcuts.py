
shortcut_arrow = "2" #Give value "1" for removing shortcut arrow or Give value "2" for restoring shortcut arrow

import os
import ctypes
import time

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)



def shortcut_remove():

    try:
        cmd=r'REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons" /v 29 /t REG_SZ /d "C:\Windows\System32\shell32.dll,49" /f'

        with disable_file_system_redirection():
            r1=os.popen(cmd).read()
        print r1
        
        print "Arrows from shortcut icons removed"
        cmd1="shutdown -r -t 00 "
        print "System will be restarted to apply changes"
        time.sleep(7)
        
        with disable_file_system_redirection():
            t1=os.popen(cmd1).read()


    except:
        print "Arrows from shortcut icons not removed"


def shortcut_restore():
    try:
        cmd=r'REG DELETE "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons" /va /f'
        with disable_file_system_redirection():
            r1=os.popen(cmd).read()
        print r1

        print "Arrows from shortcut icons restored successfully"
        cmd1="shutdown -r -t 00 "
        print "System will be restarted to apply changes"
        time.sleep(7)
        with disable_file_system_redirection():
            t1=os.popen(cmd1).read()


    except:
        print "Arrows from shortcut icons not restored"


if shortcut_arrow =="1":
    print "shortcut arrow remove is selected"
    shortcut_remove()

elif shortcut_arrow =="2":
    print "shortcut arrow restore is selected"
    shortcut_restore()

else:
    print "Shortcut arrow not configured to either remove or restore"
    


    
    
