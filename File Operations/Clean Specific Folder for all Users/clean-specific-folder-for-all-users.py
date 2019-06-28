yP=r'C:\Users\sathyadev\Downloads' # please give the folder location.
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

import subprocess        
with disable_file_system_redirection(): 
        import os

cL = yP.split(os.sep)
tempL = []
if os.path.isdir(yP):    
    if cL[1].lower() == 'users':
        rP = os.sep.join(cL[:2])
        lP = os.sep.join(cL[3:])
        aP = os.listdir(rP)
        for i in aP:
            fiP = rP+os.sep+i+os.sep+lP
            if os.path.isdir(fiP):
                tempL.append(fiP)
            else:
                pass
    else:
        print '1: It is not an User Directory'
elif os.path.isfile(yP):
    print '2: It is not an Directory'
else:
    print '3: It is not an Path'

temp = []
for tf in tempL:
    try:
        os.popen('FOR /D %p IN ("'+tf+'\\*.*") DO rd "%p" /s /q')
        os.popen('del "'+tf+'\\*" /F /Q')
        temp.append(tf)
    except:
        pass

if temp != []:
    print 'Following folders are cleaned\n'
    for i in temp:
        print i
