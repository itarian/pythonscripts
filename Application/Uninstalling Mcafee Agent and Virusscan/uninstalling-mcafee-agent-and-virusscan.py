import os
import re
import ctypes
import socket
print  "Computer Name: " +socket.gethostname()+"\n"
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
SWinfo=os.popen('wmic product get name').read()
list=[]
Find=re.search('McAfee VirusScan Enterprise',SWinfo)
if Find!=None:
    Add=Find.group()
    list.append(Add)
Find2=re.search('McAfee Agent',SWinfo)
if Find2!=None:
    Add2=Find2.group()
    list.append(Add2)
if len(list)>0:
    for i in list:
        print "Uninstalling " + i
        with disable_file_system_redirection():
            command='wmic product where name="'+i+'" call uninstall'
            Result1=os.popen(command).read()
            REG1=re.search('ReturnValue(.*)',Result1).group()
            Code=int(filter(str.isdigit, REG1))
            if Code==1603:
                print "Unistalling Failed for " + i
            elif Code==0:
                print "Uninstallation Successfull for " + i

else :
    print "McAfee VirusScan Enterprise and McAfee Agent are not installed on endpoint"
