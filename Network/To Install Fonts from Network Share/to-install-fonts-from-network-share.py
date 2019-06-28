Fontpath=r'\\AKITA-PC\latestfonts'
share_user="Akita"
share_pass="comodo"

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
import os
import shutil
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


def runvbs(vbs,cmd,Fontpath):    
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.isdir(workdir): 
        os.mkdir(workdir)
    vbs_script= vbs % ( workdir+r'\Fonts')
    with open(workdir+r'\temprun.vbs',"w") as f :
        f.write(vbs_script)        
    with disable_file_system_redirection():        
        print 'Login to network share'
        print os.popen(cmd).read()
        print 'Copying files to local machine....'
        shutil.copytree(Fontpath,workdir+r'\Fonts')        
        print os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
        print('Script execution completed successfully')
        if os.path.isfile(workdir+r'\temprun.vbs'):
            os.remove(workdir+r'\temprun.vbs')
        os.chdir(os.environ['PROGRAMDATA'])
        shutil.rmtree(workdir)


cmd= 'NET USE "'+Fontpath+'" /USER:'+share_user+'  "'+share_pass+'"'
runvbs(vbs,cmd,Fontpath) 

