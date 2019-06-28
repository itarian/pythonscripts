import os
import ctypes
import re
import shutil
if 'PROGRAMW6432' in os.environ.keys():
    path=r"C:\Program Files (x86)\COMODO\cWatchEDRAgent"
    delete=r'reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\COMODO\EDREndpoint'
else:
    path=r"C:\Program Files\COMODO\cWatchEDRAgent"
    delete=r'reg delete HKEY_LOCAL_MACHINE\SOFTWARE\COMODO\EDREndpoint'

path1=r"C:\ProgramData\COMODO\cWatchEDRAgent"

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

k=[];
with disable_file_system_redirection():
    guid=os.popen(r"wmic product get name,identifyingnumber").read();
k.append(re.findall("{.*",guid));
j=[];
for i in k[0]:
    j.append(i);
EDR=re.findall("COMODO cWatch EDR Agent",guid);
if EDR:
    with disable_file_system_redirection():
        uninst=os.popen(r"wmic product where name='COMODO cWatch EDR Agent' call uninstall").read()
        if uninst:
            print "COMODO cWatch EDR Agent Uninstalled successfully"
        else:
            print "COMODO cWatch EDR Agent not Uninstalled successfully"
else:
    print('COMODO cWatch EDR Agent not installed at Endpoint');

CMD=delete +' /va /f'
print CMD
with disable_file_system_redirection():
    out=os.popen(CMD).read()
print out

if os.path.exists(path):
    shutil.rmtree(path)
else:
    pass
if os.path.exists(path1):
    shutil.rmtree(path1)
else:
    pass
