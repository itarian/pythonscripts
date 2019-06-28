run_as_username='username'
run_as_password='********'
task_name='task name COMODO'
task_run=r'C:\windows\system32\calc.exe'
hour_at=18
minute_at=54

import subprocess
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
    process= subprocess.Popen('schtasks /create /ru %s /rp %s /sc daily /tn "%s" /tr "%s" /st %s:%s'%(run_as_username, run_as_password, task_name, task_run, str(hour_at), str(minute_at)), shell=True, stdout=subprocess.PIPE)
result=process.communicate()
ret=process.returncode
if ret==0:
    if result[0]:
        print result[0].strip()
    else:
        print result[0]
else:
    if result[1]:
        print result[1].strip()
    else:
        print result[1]
