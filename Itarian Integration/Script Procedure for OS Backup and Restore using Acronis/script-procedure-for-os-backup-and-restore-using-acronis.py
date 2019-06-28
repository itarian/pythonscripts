input=1                                #if input is 1 Backup  and  2 input is Restore
username='user1comodo'                    # Acronis Account Username   
pwd=r'Passw0rd!'                          # Acronis Account Password

ArchiveName='2042_081120171539'        #From Acronis Cloud Storage
Backupdisk="C"

#provide archive name,AcronisRecoverdrive Volume letter,AcronisTargetDrive volume letter
AcronisRecoverdrive="C"                  #give the drive name we want to recover from Acronis System Drive
AcronisTargetDrive="C"                   #give the target drive name where the drive is to be restored  As System Drive
#################################################################################################################
# IMPORTANT NOTE

#While Restoring System Drive from Acronis  Make that sure you are restoring in System drive of that TARGET MACHINE

#** If you are trying to  Restore in some other drive other than System drive the System will crash 

################################################################################################################
#Comodo copy right
#VERSION 1


import random
import time
import os
from subprocess import PIPE, Popen
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
def CMDRUN(Content):
    print "COmmand"
    print Content
    with disable_file_system_redirection():
        str(Content)
        OBJ = Popen(Content, shell = True, stdout = PIPE, stderr = PIPE)
        out, err = OBJ.communicate()
        print out
        RET = OBJ.returncode
    print RET
    if not RET:
        print out
    else:
        print err
def Backupdrive(username,pwd,d64,d86,Backupdisk):
    archivename=str(random.randint(1000, 4500))+'_'+str(time.strftime(('%d%m%Y%H%M')))
    command=r' backup disk --volume='+Backupdisk+' --loc=online:// --credentials='+username+r','+pwd+r' --arc='+archivename
    if os.path.isfile(d64):
        print "64 bit machine"
        Content=r""+'"'+""+d64+'"'+" "+command
    elif os.path.exists(d86):
        print Content
        Content=r""+'"'+""+d86+'"'+" "+command
    else:
        Content=None
    
    if not Content:
        print 'acronis backup commandline utitlity is not installed :('
    else:
        CMDRUN(Content)
def recoverdrive(ArchiveName,AcronisRecoverdrive,AcronisTargetDrive,username,pwd,d64,d86):
    command=r' recover disk  --loc=online:// --credentials='+username+r','+pwd+r' --arc='+ArchiveName +" --volume="+AcronisRecoverdrive+" --target_volume="+AcronisTargetDrive+" --silent_mode=on --reboot"
    if os.path.isfile(d64):
        print "64 bit machine"
        Content=r""+'"'+""+d64+'"'+" "+command
    elif os.path.exists(d86):
        print Content
        Content=r""+'"'+""+d86+'"'+" "+command
    else:
        Content=None
    
    if not Content:
        print 'Acronis backup commandline utitlity is not installed :('
    else:
        CMDRUN(Content)
    
try :
    os.chmod(r'C:\Users\Acronis Agent User', 0777)
except:
    pass
  

d64=r'C:/Program Files/BackupClient/CommandLineTool/acrocmd.exe'
d86=r'C:/Program Files (x86)/BackupClient/CommandLineTool/acrocmd.exe'
Backupdisk="C" 
if input==1:
    print "Backing up the drive"
    Backupdrive(username,pwd,d64,d86,Backupdisk)
elif input==2:
    
    print "Restoring the drive"
    recoverdrive(ArchiveName,AcronisRecoverdrive,AcronisTargetDrive,username,pwd,d64,d86)

else:
    print "Please Enter Valid Parameter"
    print "Give Input 1 for Backing up the OS"
    print "Give Input 2 for Restoring The OS"
    
