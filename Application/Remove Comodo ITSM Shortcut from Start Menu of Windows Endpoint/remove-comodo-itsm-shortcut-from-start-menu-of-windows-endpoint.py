import os 
import shutil
import ctypes
user_path=os.environ['APPDATA']
prdata=os.environ['PROGRAMDATA']

itsmlink_1=prdata+"\Microsoft\Windows\Start Menu\Programs\Comodo ITSM.lnk"
itsmlink_2=user_path+r"\Microsoft\Windows\Start Menu\Programs\Comodo ITSM.lnk"

itsm=prdata+r"\Microsoft\Windows\Start Menu\Programs\Comodo"

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
    try:
        if os.path.isdir(itsm):
            shutil.rmtree(itsm,ignore_errors=True)
            os.rmdir(itsm)
            print os.popen(itsm+' /s /q').read()
    except:
        pass

    if os.path.isfile(itsmlink_1):
        os.remove(itsmlink_1)
        print('Comodo ITSM has been removed from start menu')

    if os.path.isfile(itsmlink_2):
        os.remove(itsmlink_2)
        print('Comodo ITSM has been removed from start menu')

    out=os.popen('REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /V "Start_NotifyNewApps" /t  REG_DWORD /d 0 /F').read()
    print (out)

    print("Highlighting recently installed program has been disabled")

