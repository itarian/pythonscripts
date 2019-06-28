url=r'http://webpagepublicity.com/free-fonts/x/Xerox%20Sans%20Serif%20Narrow.ttf' #Provide the website url which you need to install as a font
fileName='Narrow.ttf' # Provide the filename of the font

import os
import ssl
import urllib2
import shutil
import ctypes

ssl._create_default_https_context = ssl._create_unverified_context
temp=os.environ['PROGRAMDATA']+r'\c1_temp'

if not os.path.exists(temp):
    os.makedirs(temp)



vbs=r'''
Set objShellApp = CreateObject("Shell.Application")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Const FONTS = &H14&
Set objFolder = objShellApp.Namespace(FONTS)
strNewFontsFolder = "%s"
If objFSO.FolderExists(strNewFontsFolder) = True Then    
 For Each objFile In objFSO.GetFolder(strNewFontsFolder).Files  
  If LCase(right(objFile,4)) = ".ttf" OR LCase(right(objFile,4)) = ".otf" Then      
   If objFSO.FileExists(objFolder.Self.Path & "\" & objFile.Name) = False Then objFolder.CopyHere objFile.Path
   Wscript.Echo "Installed  " & objFile.Name
  End If
    Next
Else
    Wscript.Echo  "Unable to find " & strWindowsFonts
End If

'''

def Download(temp,url):
    fp = os.path.join(temp, fileName)
    request = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(temp):
        pass
    if not os.path.exists(temp):
        os.makedirs(temp)
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    return fp

Fontpath=Download(temp,url)

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


def runvbs(vbs,Fontpath):    
    if not os.path.isdir(temp): 
        os.mkdir(workdir)
    vbs_script= vbs % (temp)
    with open(temp+r'\temprun.vbs',"w") as f :
        f.write(vbs_script)        
    with disable_file_system_redirection():              
        print os.popen('cscript.exe "'+temp+r'\temprun.vbs"').read()
        print('Script execution completed successfully')
        if os.path.isfile(temp+r'\temprun.vbs'):
            os.remove(temp+r'\temprun.vbs')

    try:
        shutil.rmtree(temp)

    except:
        pass

runvbs(vbs,Fontpath)        
