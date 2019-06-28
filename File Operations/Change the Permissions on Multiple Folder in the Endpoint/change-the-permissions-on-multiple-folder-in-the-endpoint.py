#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('variableName') with that parameter's name
path=itsm.getParameter('PATH') #please provide the path to the directory or folder
user=itsm.getParameter('USER')   #please provide the username 
permission=itsm.getParameter('PERMISSION')   #Please provide any one of the following permission rights

                  #F - full access
                  #M - modify access
                  #RX - read and execute access
                  #R - read-only access
                  #W - write-only access
                  #D - delete access


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


if os.path.exists(path):
    with disable_file_system_redirection():
        cmd=os.popen('icacls "%s" /grant %s:(OI)(CI)%s /T'%(path,user,permission)).read()
        if "Failed processing 0" in cmd:
            print "Folders permission changed sucessfully"
        else:
            print "Error occured"
else:
    print "Please Enter the valid folder path"
