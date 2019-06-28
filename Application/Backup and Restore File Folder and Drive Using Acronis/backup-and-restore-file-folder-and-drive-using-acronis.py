###############INPUT SECTION############################

input=itsm.getParameter('input')
#if input is 1 or 2 define backup path
username=itsm.getParameter('username')
pwd=itsm.getParameter('acronisaccountpassword') 
BackupPathfile=itsm.getParameter('BackuppathforFile')
BackupPathfolder=itsm.getParameter('BackupPathfolder')
#If your input is 3 provide Volume Name
Backupdisk=itsm.getParameter('Backupdisk')
#If your input is 4 or 5 provide Archive Name,acronispath,RecoverydestinationPath
ArchieveName=itsm.getParameter('newtestarchive') 
acronispath=itsm.getParameter('acronispath')
RecoverydestinationPath=itsm.getParameter('RecoverydestinationPath') 
#If your input is 6 provide archive name,AcronisRecoverdrive Volume letter,AcronisTargetDrive volume letter
AcronisRecoverdrive=itsm.getParameter('AcronisRecoverdrive')
AcronisTargetDrive=itsm.getParameter('AcronisTargetDrive')
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
def Backupfileorfolder(username,pwd,BackupPath,d64,d86):
    archivename=str(random.randint(1000, 4500))+'_'+str(time.strftime(('%d%m%Y%H%M')))
    command=r' backup file --include="'+BackupPath+'" --loc=online:// --credentials='+username+r','+pwd+r' --arc='+archivename
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

def recoverfileorfolder(ArchieveName,acronispath,RecoverydestinationPath,username,pwd,d64,d86):
    print "REcovering"
    command=r' recover file  --loc=online:// --credentials='+username+r','+pwd+r' --arc='+ArchieveName +" --file="+acronispath+" --target="+RecoverydestinationPath
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
def recoverdrive(ArchieveName,AcronisRecoverdrive,AcronisTargetDrive,username,pwd,d64,d86):
    
    
    command=r' recover disk  --loc=online:// --credentials='+username+r','+pwd+r' --arc='+ArchieveName +" --volume="+AcronisRecoverdrive+" --target_volume="+AcronisTargetDrive
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

if input==1:
    print "Backing up the folder"
    Backupfileorfolder(username,pwd,BackupPathfolder,d64,d86)
elif input==2:
    BackupPathfile='"'+BackupPathfile+'"'
    print "Backing up the file"
    Backupfileorfolder(username,pwd,BackupPathfile,d64,d86)
elif input==3:
    print "Backing up the DRIVE"
    Backupdrive(username,pwd,d64,d86,Backupdisk)
elif input==4:
    print "Recovering up the folder"
    recoverfileorfolder(ArchieveName,acronispath,RecoverydestinationPath,username,pwd,d64,d86)
elif input ==5:
    print "Recovering up the File"
    recoverfileorfolder(ArchieveName,acronispath,RecoverydestinationPath,username,pwd,d64,d86)
elif input==6:
    recoverdrive(ArchieveName,AcronisRecoverdrive,AcronisTargetDrive,username,pwd,d64,d86)
    print "Recovering up the drive"
else:
    print "Please Enter Valid Parameter"
    print "Give Input 1 for Backing up the folder"
    print "Give Input 2 for Backing up the file"
    print "Give Input 3 for Backing up the Disk"
    print "Give input 4 for Recovering up the folder"
    print "Give input 5 for Recovering up the File"
    print "Give input 6 for Recovering up the Drive"
