# Please use "alert(1)" to turn on the monitor(trigger an alert) 
# Please use "alert(0)" to turn off the monitor(disable an alert) 
#This script is used to Check the Bit Locker Drive Encryption and Decryption status

import os,re,ctypes,sys,subprocess
from subprocess import PIPE,Popen
def alert(arg): 
	sys.stderr.write("%d%d%d" % (arg, arg, arg))
def checkdrive():
    ps_command=r'manage-bde -status '+i+":"
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
         process=subprocess.Popen('powershell "%s"'%ps_command, shell=True, stdout=subprocess.PIPE)
    result=process.communicate()
    if not "ERROR:" in result[0]:
        print ps_command
        m=result[0].strip()
        n=re.findall('Conversion\sStatus:\s\s\s\s(.*)',m)
        percent=re.findall('Percentage\sEncrypted:\s(.*)',m)
        percent=percent[0].strip()
        out=n[0].strip()
        li=[]
        if "Fully Decrypted" in out:
            print "Bitlocker is not enabled for "+i+ " Drive"
            li.append("No")
        else:
            if "Used Space Only Encrypted" in out:
                print "The used space is Encrypted fully in "+i+ " drive"
                print percent
                li.append("yes")
            elif "Fully Encrypted" in out:
                print "The"+i+" Drive is fully encrypted"
                print percent
                li.append("yes")
            elif "Encryption in Progress" in out:
                print "The "+i+" Drive  Encryption is in progress"
                print percent
                li.append("yes")
            elif "Decryption in Progress" in out:
                print i+"Decryption is in progress"
                print percent
                li.append("yes")
        return li

file1=os.environ['programdata']+"\\"+"script.txt"
with open(file1,"wb") as e:
    e.write("list volume")

ps_cmd="Get-WindowsFeature -Name BitLocker* | Where InstallState -Eq Installed"
check=os.popen("wmic os get Caption").read()
if "Server" in check:
    a= os.popen('powershell "%s"'%ps_cmd).read()
    if len(a)>0:
        if "BitLocker Drive Encryption" in a:
            checkDrive=os.popen('diskpart /s "C:\\ProgramData\\script.txt"').read()
            c=re.findall("\s\s\s[a-zA-Z]\s\s\s",checkDrive)
            c2=''.join(c)
            c1=re.findall("[a-zA-Z]",c2)
            for i in c1:
                c3=checkdrive()
            if not "yes" in str(c3):
                alert(1)
            else:
                alert(0)
    else:
            print "Bitlocker is not activated"
            alert(0)
else:
    checkDrive=os.popen('diskpart /s "C:\\ProgramData\\script.txt"').read()
    c=re.findall("\s\s\s[a-zA-Z]\s\s\s",checkDrive)
    c2=''.join(c)
    c1=re.findall("[a-zA-Z]",c2)
    for i in c1:
        c3=checkdrive()
    if not "yes" in str(c3):
        alert(1)
    else:
        alert(0)
        


try:
    os.remove(file1)
except:
    pass
