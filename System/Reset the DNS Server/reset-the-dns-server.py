preferred_dns_server=r"8.8.4.4"
import os
import re
import subprocess
import ctypes
intr=os.popen("wmic nic get NetConnectionid" ).read()
Name=[i.strip() for i in  intr.split("\n") if i.strip()]
a=Name[1:][-1]
addr='netsh interface ipv4 show addresses "%s"'%a
addr1=os.popen(addr).read()
reset='netsh interface ip set dns "%s" dhcp'%a
print ("DNS Server is reset")
print("CHANGING DNS SERVER FROM AUTOMATIC TO MANUAL")
bat=r'''
netsh interface ip set dns name="%s" static %s 
'''%(a,preferred_dns_server)

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

path=os.environ['programdata']+"\Sample.bat"
with open(path,"w") as f:
    f.write(bat)
    
with disable_file_system_redirection():
 process = subprocess.Popen([path],stdout=subprocess.PIPE)
 stdout = process.communicate()[0]
 print "--------------------------------------------"
 
if os.path.exists(path):
 try:
  os.remove(path)
 except:
  pass

print("Now the Dns server has changed from automatic to manual")
