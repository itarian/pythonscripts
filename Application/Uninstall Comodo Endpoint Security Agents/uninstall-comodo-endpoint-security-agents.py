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
 
k=[];
with disable_file_system_redirection():
    guid=os.popen('powershell.exe "get-wmiobject Win32_Product | Format-Table Name,IdentifyingNumber" |  findstr /i /c:"COMODO Endpoint Security" /c:"COMODO ESM Agent"| sort').read();
print (guid);
k.append(re.findall("{.*",guid));
j=[];
for i in k[0]:
   j.append(i);
print j;
ces=re.findall("COMODO Endpoint Security",guid);
cesm=re.findall("COMODO ESM Agent",guid);
if (ces and cesm):
    command=r"reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\CmdAgent\Mode /v ModeEsm /t REG_DWORD  /d  1  /f";
    with disable_file_system_redirection():
        reg_process=os.popen(command).read();
        print(reg_process);
        ces_out=os.popen('msiexec.exe /x '+j[0]+' /quiet REBOOT=ReallySuppress REMOVE=ALL CESMCONTEXT=1').read();
        print(ces_out)
        process=os.popen('msiexec.exe /x '+j[1]+' /quiet REBOOT=ReallySuppress REMOVE=ALL').read();
        print (process);
    
elif cesm:
    with disable_file_system_redirection():
        process=os.popen('msiexec.exe /x '+j[0]+' /quiet REBOOT=ReallySuppress REMOVE=ALL').read();
        print (process);
else:
   print('No installation found');