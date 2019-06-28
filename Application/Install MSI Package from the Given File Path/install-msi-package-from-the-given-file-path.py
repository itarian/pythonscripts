#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name
msi_file_path=itsm.getParameter('parameterName')

import os
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

if os.path.isfile(msi_file_path):        
    with disable_file_system_redirection():
        process= subprocess.Popen('msiexec /i "%s" /qn'%msi_file_path, shell=True, stdout=subprocess.PIPE)
    result=process.communicate()
    ret=process.returncode
    if ret==0:
        print result[0]
        print "%s file is installed successfully"%msi_file_path
    else:
        print result[1]
        print "%s file is installed with return code 1"%msi_file_path
else:
    print '%s is not found.'%msi_file_path
