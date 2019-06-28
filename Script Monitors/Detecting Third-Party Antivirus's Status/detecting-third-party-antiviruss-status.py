import os
import subprocess
import ctypes
import re
import sys

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))
   
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
     r=os.popen(r'WMIC /Node:localhost /Namespace:\\root\SecurityCenter2 Path AntiVirusProduct Get "displayName","productState" /Format:List').read()
     r=r.strip('\r\n')
     
     if r == '':
         ale = ale +1
         print " No antivirus installed in the System"
     else:
        reg="displayName=(.*)"
        reg1="productState=(.*)"

        name=re.findall(reg,r)
        
        product=re.findall(reg1,r)
        
        list=[]

        for ind,j in  enumerate(name):
            list.append(j+"="+product[ind])
        li=[]
        for i in list:
            prod=re.findall("=(.*)",i)[0]
            prod=int(prod)
            a=hex(prod)
            y=a[-4:]
            f1="yes"
            f="No"
            if(y=="0000"):
                li.append(f)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Disabled and Up-to-date")
            if(y=="0010"):
                li.append(f)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Disabled and not Up-to-date")
            if(y=="1000"):
                li.append(f1)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Enabled and Up-to-date")
            if(y=="1010"):
                li.append(f)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Enabled and not Up-to-date")
            if(y=="2000"):
                li.append(f)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Disabled and Up-to-date")
            if(y=="2010"):
                li.append(f)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Disabled and not Up-to-date")
            if(y=="1100"):
                li.append(f1)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Enabled and Up-to-date")
            if(y=="2100"):
                li.append(f)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is disabled and Up-to-date")
            if(y=="0100"):
                li.append(f)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is disabled and Up-to-date")
            if(y=="1110"):
                li.append(f)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Enabled and not Up-to-date")
            if(y=="2110"):
                li.append(f)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is disabled and not Up-to-date")
            if(y=="0110"):
                li.append(f)
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+"has been turned off and is not monitoring your computer")


if "No" in li:
   alert(1)
else:
   alert(0)
