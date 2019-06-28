import os
vbs=r'''Set objShell = WScript.CreateObject("WScript.Shell")
allUsersDesktop = objShell.SpecialFolders("AllUsersDesktop")
Set objShortCut = objShell.CreateShortcut(allUsersDesktop & "\Notepad.lnk")
objShortCut.TargetPath = "%SystemRoot%\system32\notepad.exe"
objShortCut.Description = "Run the Notepad."
objShortCut.Save'''
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


