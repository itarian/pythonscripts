BAT=r'''
ipconfig
'''
import os
import sys
import platform
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

path=os.environ['programdata']+"\Sample.bat"
with open(path,"w") as f:
    f.write(BAT)
try:
    with disable_file_system_redirection():
            print "Excuting Bat File"
            process = subprocess.Popen([path],stdout=subprocess.PIPE)
            stdout = process.communicate()[0]
            print "---------------------------"
            print stdout

except:
    print "Excuting Bat File"
    process = subprocess.Popen([path],stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    print "---------------------------"
    print stdout

    
if os.path.exists(path):
	try:
		os.remove(path)
	except:
		pass
