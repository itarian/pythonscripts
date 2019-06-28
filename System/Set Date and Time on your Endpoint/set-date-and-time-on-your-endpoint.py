Date='7/20/2018' # Provide date in this format(mm/dd/yyyy) mm - month, dd - date, yyyy - year
Time='6:36:00 PM' #Provide time in this format (h:m:s AM/PM) h - hour, m- minute, s- second along with 12 hour format (AM/PM) 

import os
import ctypes
import _winreg
import datetime
workdir=os.environ['PROGRAMDATA']+r'\temp'

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

vbs=r'''with CreateObject("Wscript.Shell")
.Run "%comspec% /c date {}"
.Run "%comspec% /c time {}"
end with
'''.format(Date,Time)

def runvbs(vbs):
    if not os.path.isdir(workdir): 
        os.mkdir(workdir)
    with open(workdir+r'\temprun.vbs',"w") as f :
        f.write(vbs)        
    with disable_file_system_redirection():
        print os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
        print('Script execution completed successfully')
        print "Time and Date changed Successfully"


runvbs(vbs)

with disable_file_system_redirection():
    keyVal = r'SOFTWARE\Policies\Microsoft\Control Panel\International'

key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,keyVal)
_winreg.SetValueEx(key, "PreventUserOverrides", 0,_winreg.REG_DWORD,1)
_winreg.CloseKey(key)

now = datetime.datetime.now()
date=now.strftime("%Y-%m-%d")
time=now.strftime("%H:%M")

if os.path.isfile(workdir+r'\temprun.vbs'):
    os.remove(workdir+r'\temprun.vbs')


