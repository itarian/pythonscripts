#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name
caption=itsm.getParameter('parameterName')
message=itsm.getParameter('parameterName1')
 
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
			
def legalnotice(caption,message):
    with disable_file_system_redirection():
        wcaption=os.popen(r'reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v legalnoticecaption /t REG_SZ /d  "'+caption+'"  /f ').read()
        print(wcaption);
        wtext=os.popen(r'reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v legalnoticetext  /t REG_SZ /d  "'+message+'" /f ').read()
        print(wtext);

legalnotice(caption,message)
