username="********"     ## enter the username of the device you need to map
password="********"       ##enter the password of that device
DriveLetter = 'Y:'     ##enter the drive you want to map
SharedNetworkPath = r'\\DESKTOP-3HLBO2K\Users\thunderbolt\Documents\Malz2'## enter the path of shared folderimport subprocess
name=SharedNetworkPath.split("\\")[-1]

import os;
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
with disable_file_system_redirection():
    x=os.popen("wmic logicaldisk where DriveType='4' get description,name").read().split()
    w=set(x)
    if w:
        w.remove('Description')
        w.remove('Name')
        w.remove('Network')
        w.remove('Connection')
        c=list(w)
        if DriveLetter in c :
            print("The drive "+DriveLetter+" already exists")
            print os.popen('net use').read()
            print("please try someother drive letter....")
        else:
            set=os.popen('reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system /v EnableLinkedConnections /t REG_DWORD /d 1 /f').read();
            p = 'net use '+DriveLetter+' '+SharedNetworkPath+' /user:'+username+' '+password+' /persistent:yes /YES' 
            z = os.popen(p).read()
            print z
##            print "The drive "+DriveLetter+" is now connected to the "+SharedNetworkPath+"."
            ##x=os.popen('net use').read()
            ##print x
    else:
        set=os.popen('reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system /v EnableLinkedConnections /t REG_DWORD /d 1 /f').read();
        p = 'net use '+DriveLetter+' '+SharedNetworkPath+' /user:'+username+' '+password+' /persistent:yes /YES' 
        z = os.popen(p).read()
        print z
        print "The drive "+DriveLetter+" is now connected to the "+SharedNetworkPath+" sharepath."
        ##x=os.popen('net use').read()
        ##print x
    
##to create the shortcut
vbs=r'''Set objShell = WScript.CreateObject("WScript.Shell")
allUsersDesktop = objShell.SpecialFolders("AllUsersDesktop")
Set objShortCut = objShell.CreateShortcut(allUsersDesktop & "\%s.lnk")
objShortCut.TargetPath = "%s\"
objShortCut.Description = "Mapped Drive Shortcut"
objShortCut.Save'''%(name,DriveLetter)
def runvbs(vbs):
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.isdir(workdir): 
        os.mkdir(workdir)
    with open(workdir+r'\temprun.vbs',"w") as f :
        f.write(vbs)        

    print os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
    print('Script execution completed successfully')
    if os.path.isfile(workdir+r'\temprun.vbs'):
        os.remove(workdir+r'\temprun.vbs')

runvbs(vbs) 
