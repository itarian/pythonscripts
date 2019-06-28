import os
import subprocess
import ctypes
import re
import sys

ale =0
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

        for i in list:
            prod=re.findall("=(.*)",i)[0]
            prod=int(prod)
            a=hex(prod)
            
            y=a[-4:]

            
            if(y=="0000"):
                ale = ale+1
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Disabled ")
            elif(y=="0010"):
                ale = ale+1
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Disabled ")
            elif(y=="1000"):
                ale = 0
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Enabled ")
            elif(y=="1010"):
                ale = 0
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Enabled ")
            elif(y=="2000"):
                ale = ale+1
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Disabled ")
            elif(y=="2010"):
                ale = ale+1
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Disabled ")
            elif(y=="1100"):
                ale = 0
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Enabled ")
            elif(y=="2100"):
                ale = ale+1
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is disabled ")
            elif(y=="1110"):
                ale = 0
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is Enabled ")
            elif(y=="2110"):
                ale = ale+1
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+" is disabled ")
            elif(y=="0110"):
                ale = ale+1
                Antivirus=re.findall("(.*)=",i)[0]
                print(Antivirus+"has been turned off and is not monitoring your computer")

                
if ale>=1:
    alert(1)
else:
    alert(0)
