URL='http://www.iconarchive.com/download/i50371/hopstarter/orb/Internet-Explorer.ico' #Give the Download icon URL
src_path="C:\Users\win732dt\Downloads\icon" #Give the preferred path location
import os
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
import urllib
def Download(src_path, URL):
    import urllib2
    import os
    print "Icon Download started"
    fileName = '1.ico'#Give any icon file name as per your wish
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(src_path):
        print "icon downloaded Path already exists"
    if not os.path.exists(src_path):
        os.makedirs(src_path)
        print "icon downloaded Path created"
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    print "The file downloaded successfully in specified path"
    return fp
si=Download(src_path, URL)
de= '"'+si+'"'
print de
vbs=r'''
Dim WshProcEnv
Dim process_architecture
Set WshShell = WScript.CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("AllUsersDesktop")
Set WshProcEnv = WshShell.Environment("Process")
Set oShellLink = WshShell.CreateShortcut(strDesktop & "\Internet Explorer.lnk")
process_architecture= WshProcEnv("PROCESSOR_ARCHITECTURE") 
If process_architecture = "x86" Then
    oShellLink.TargetPath = "C:\Program Files\Internet Explorer\iexplore.exe"
Else
    oShellLink.TargetPath = "C:\Program Files (x86)\Internet Explorer\iexplore.exe"
End If
oShellLink.WindowStyle = 1
oShellLink.IconLocation = %s
oShellLink.Hotkey = "CTRL+SHIFT+F"
oShellLink.Description = "Shortcut Script"
oShellLink.WorkingDirectory = strDesktop
oShellLink.Arguments = "https://www.google.com"
oShellLink.Save
'''% (de)
def runvbs(vbs):
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.isdir(workdir): 
        os.mkdir(workdir)
    with open(workdir+r'\temprun.vbs',"w") as f :
        f.write(vbs)        
    with disable_file_system_redirection():
        print os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
        print('Script execution completed successfully')
    if os.path.isfile(workdir+r'\temprun.vbs'):
        os.remove(workdir+r'\temprun.vbs')

runvbs(vbs) 


