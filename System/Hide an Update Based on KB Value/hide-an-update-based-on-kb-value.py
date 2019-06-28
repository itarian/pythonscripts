KB="KB3172729"   # Enter the KB value of patch which you want to hide.


import os
import re
import ctypes
import time
import subprocess
from subprocess import PIPE, Popen

vbs=r'''Dim WSHShell, StartTime, ElapsedTime, strUpdateName, strAllHidden
Dim Checkagain 'Find more keep going otherwise Quit

Dim hideupdates(0) 

hideupdates(0) = "%s"


Set WSHShell = CreateObject("WScript.Shell")

StartTime = Timer 'Start the Timer

Set updateSession = CreateObject("Microsoft.Update.Session")
updateSession.ClientApplicationID = "MSDN Sample Script"
Set updateSearcher = updateSession.CreateUpdateSearcher()
Set searchResult = updateSearcher.Search("IsInstalled=0 and Type='Software' and IsHidden=0")

Checkagain = "True"

For K = 0 To 10 'Bing Desktop has 4, Silverlight has 5
If Checkagain = "True" Then
Checkagain = "False"
CheckUpdates
ParseUpdates
End if
Next

ElapsedTime = Timer - StartTime
strTitle = "Bing Desktop and Windows Updates Hidden."
strText = strAllHidden
strText = strText & vbCrLf & ""
strText = strText & vbCrLf & "Total Time " & ElapsedTime
intType = vbOkOnly

Set objWshShell = nothing
Set WSHShell = Nothing
WScript.Quit


Function ParseUpdates 'cycle through updates
For I = 0 To searchResult.Updates.Count-1
Set update = searchResult.Updates.Item(I)
strUpdateName = update.Title
'WScript.Echo I + 1 & "> " & update.Title
For j = 0 To UBound(hideupdates)
if instr(1, strUpdateName, hideupdates(j), vbTextCompare) = 0 then
Else
strAllHidden = strAllHidden _
& vbcrlf & update.Title
update.IsHidden = True'
Checkagain = "True"
end if
Next
Next
End Function

Function CheckUpdates
Set updateSession = CreateObject("Microsoft.Update.Session")
updateSession.ClientApplicationID = "MSDN Sample Script"
Set updateSearcher = updateSession.CreateUpdateSearcher()
Set searchResult = _
updateSearcher.Search("IsInstalled=0 and Type='Software' and IsHidden=0")
End Function
'''

try:
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)      
except:
    workdir=os.environ['SYTEMDRIVE']

        
def Hide_update():
    import os

    script =vbs % (KB)

    with open(workdir+r'\Hide_windowsupdate.vbs',"w") as f :
        f.write(script)        


    obj = subprocess.Popen('cscript.exe "'+workdir+'\Hide_windowsupdate.vbs"', shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    print out

    try:
        if os.path.isfile(workdir+r'\Hide_windowsupdate.vbs'):
            os.remove(workdir+r'\Hide_windowsupdate.vbs')

    except: 
        pass


def check_status(KB):
    Ps='''(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search('IsHidden=1').Updates | %{'KB'+$_.KBArticleIDs}'''

    with open(workdir+r'\Hide_windowsupdate.ps1',"w") as f :
        f.write(Ps)
    CMD='powershell "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"'
    Ki=subprocess.Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    obj = subprocess.Popen('powershell.exe "'+workdir+r'\Hide_windowsupdate.ps1"', shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    if KB in out:
        print "Specified KB update has been Hidden successfully"
    else:
        print "Please ensure that entered KB update is present in available Updates list"
    

    try:
        if os.path.isfile(workdir+r'\Hide_windowsupdate.ps1'):
            os.remove(workdir+r'\Hide_windowsupdate.ps1')

    except: 
        pass

    
Hide_update()
time.sleep(60)
check_status(KB)
