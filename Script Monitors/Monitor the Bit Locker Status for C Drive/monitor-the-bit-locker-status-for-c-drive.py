Drive='C'

#This script is used to Check the Bit Locker Drive Encryption and Decryption status
#Please Enter the Drive you want to check the  Bitlocker Encryption status


ps_command=r'manage-bde -status '+Drive+':' 
print ps_command

import os,re
import subprocess,sys,ctypes
from subprocess import PIPE,Popen

def alert(arg): 
	sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

# Please use "alert(1)" to turn on the monitor(trigger an alert) 
# Please use "alert(0)" to turn off the monitor(disable an alert) 
# Please do not change above block and write your script below


def checkdrive():
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
    ret=process.returncode
    

    if ret==0:
        if result[0]:
            m=result[0].strip()
            n=re.findall('Conversion\sStatus:\s\s\s\s(.*)',m)
            percent=re.findall('Percentage\sEncrypted:\s(.*)',m)
            percent=percent[0].strip()
            out=n[0].strip()
        
            if "Fully Decrypted" in out:
                print "Bitlocker is not enabled for "+Drive+" Drive"
                alert(1)
            else:
                if "Used Space Only Encrypted" in out:
                    print "The used space is Encrypted fully"
                    print percent
                    alert(0)
                elif "Fully Encrypted" in out:
                    print "The"+Drive+" Drive is fully encrypted"
                    print percent
                    alert(0)
                elif "Encryption in Progress" in out:
                    print "The "+Drive+" Drive  Encryption is in progress"
                    print percent
                    alert(0)
                elif "Decryption in Progress" in out:
                    print Drive+"Decryption is in progress"
                    print percent
                    alert(0)
        else:
            print None
            
    else:
        print '%s\n%s'%(str(ret), str(result[1]))

checkDrive=os.popen('wmic logicaldisk get description,name|findstr "Local Fixed Disk"').read()
##print checkDrive
if Drive in checkDrive:
    checkdrive()
else:
    print "Entered drive " +Drive+" does not occurs in the system."
    alert(1)
