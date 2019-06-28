import os
import ctypes
from subprocess import PIPE, Popen

def oscmd(command):
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
        obj = os.popen(command).read()
    return obj.strip()

result=''
detected_drives=oscmd('wmic logicaldisk get name')
required_drive_letters=[i.strip() for i in detected_drives.split('\n') if i.strip()][1:]
os_drive=os.environ['SYSTEMDRIVE']
required_drive_letters.remove(os_drive)
if required_drive_letters:
    for i in required_drive_letters:
        other_drive_fix=oscmd('chkdsk %s /f'%i)
        trimed_other_drive_fix=''
        if other_drive_fix:
            for a in other_drive_fix.split('\r'):
                if 'progress' not in a.lower() and 'percent' not in a.lower():
                    if a.strip():
                        trimed_other_drive_fix+=a
        result+='%s\n%s\n%s\n\n'%('Result of [%s] Drive: '%i, '.'*30, trimed_other_drive_fix)
osdrive_fix=oscmd('echo yes | chkdsk %s /f'%os_drive)
trimed_osdrive_fix=''
for a in osdrive_fix.split('\r'):
    if 'progress' not in a.lower() and 'percent' not in a.lower():
        if a.strip():
            trimed_osdrive_fix+=a
result+='%s\n%s\n%s'%('Result of [%s] Drive: '%os_drive, '.'*30, osdrive_fix)
print result
