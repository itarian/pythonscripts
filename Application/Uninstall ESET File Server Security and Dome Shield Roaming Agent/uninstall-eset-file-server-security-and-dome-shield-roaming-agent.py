import os;
import re;
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
#to uninstall dome shield agent
k=[];
with disable_file_system_redirection():
    guid=os.popen('wmic product get name,IdentifyingNumber | sort').read();
k.append(re.findall("{.*",guid));
j=[];
for i in k[0]:
	j.append(i);
ces=re.findall("Shield Agent",guid);
if ces:
    with disable_file_system_redirection():
        process=os.popen('wmic product where name="Comodo Shield Agent" call uninstall ').read();
        print "Dome shield agent uninstallation Successful"
else:
	print('Dome shield agent is not installed at endpoint');
#to uninstall ESET file security 
k=[];
with disable_file_system_redirection():
    guid=os.popen('wmic product get name,IdentifyingNumber | sort').read();
k.append(re.findall("{.*",guid));
j=[];
for i in k[0]:
	j.append(i);
ces=re.findall("ESET File Security",guid);
if ces:
    with disable_file_system_redirection():
        process=os.popen('wmic product where name="ESET File Security" call uninstall').read();
        print "ESET File Security uninstallation Successful"
else:
	print('ESET File Security is not installed at endpoint');


