import os

vbs=r'''
Dim fso,logfile, iReboot, bMSReboot, appendout
logfile = "%s"	'Name of log file.
Const ForAppend = 8
Set fso = CreateObject("Scripting.FileSystemObject")
Dim WshShell: Set WshShell = WScript.CreateObject("WScript.Shell")
iReboot = 0
On Error Resume Next
Set appendout = fso.OpenTextFile(logfile, ForAppend, True)
WriteLog "Launched with do not reboot"

Set oSession = CreateObject("Microsoft.Update.Session")

Set updateSearcher = oSession.CreateupdateSearcher
If Err <> 0 Then
	WriteLog "Update Searcher not created" & Err.Description
	WScript.Quit
End If 

Set searchResult = updateSearcher.Search("IsInstalled=0 and Type='Software'")
If Err <> 0 Then
	WriteLog "Update Search function failed."&  Err.Description
	WScript.Quit
End If 

If searchResult.Updates.Count = 0 Then
	WriteLog "There are no applicable updates."
	WScript.Quit
End If

'Creating collection of updates to download
Set updatesToDownload = CreateObject("Microsoft.Update.UpdateColl")

For I = 0 to searchResult.Updates.Count-1
    Set update = searchResult.Updates.Item(I)
	Set objCategories = update.Categories
	strCatName = lcase(objCategories.Item(0).Name)

	If 	strCatName = "security updates" Or _
		strCatName = "critical updates" Or _
		InStr(strCatName,"office") And 	InStr(update.description,"security") Then 
    WriteLog "adding " & update.Title & " to download list."
		updatesToDownload.Add(update) 
	End If 
Next

'Downloading updates...
If updatestoDownload.count = 0 Then
	WriteLog "No critical or security patches found to download, quitting."
	WScript.Quit
End If
Set downloader = oSession.CreateUpdateDownloader() 

downloader.Updates = updatesToDownload
downloader.Download()

Set updatesToInstall = CreateObject("Microsoft.Update.UpdateColl")

'Creating collection of downloaded updates to install

For I = 0 To searchResult.Updates.Count-1
    set update = searchResult.Updates.Item(I)
    If update.IsDownloaded  Then
	    WriteLog "adding " & update.Title & " to install list."
	    updatesToInstall.Add(update)	
    End If
Next

WriteLog "Installing updates..."
Set installer = oSession.CreateUpdateInstaller()
installer.Updates = updatesToInstall
Set installationResult = installer.Install()

'Output results of install
WriteLog "Installation Result: " &	Code2Text(installationResult.ResultCode)
WriteLog  "Reboot Required: " & installationResult.RebootRequired 
bMSReboot = installationResult.RebootRequired
strMessage = "Listing of updates installed " & _
 "and individual installation results:"  & VbCrLf 

For I = 0 to updatesToInstall.Count - 1
	strMessage =  VbCrLf & strMessage & vbtab & updatesToInstall.Item(i).Title & _
	": " & code2text(installationResult.GetUpdateResult(i).ResultCode) & vbNewLine
	 
Next

WriteLog strMessage

If bMSReboot = False then 
	strmessage ="Done.  No reboot required"
Else
	If iReboot = 2 Then strmessage = "Done.  Logged on user, not rebooting computer"
	If iReboot = 0 Then strmessage = "Done.  Not rebooting computer"			
End If 

WriteLog strmessage



Sub WriteLog (message)
	message = now & vbTab &  message
	AppendOut.WriteLine message
End Sub  


Function Code2Text(iCode)
	If iCode = 2 Then 
		Code2Text = "Okay"
	Else
		Code2Text = "Failed"
	End If 
End Function 
'''

try:
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)      
except:
    workdir=os.environ['SYTEMDRIVE']


    
logpath=workdir+r'\update_log.txt'
script =vbs % (logpath)

with open(workdir+r'\windowsupdate.vbs',"wb") as f :
    f.write(script)        

print os.popen('cscript.exe "'+workdir+'\windowsupdate.vbs"').read()

with open(logpath,"r") as fr :
    out=fr.read()        

print out

try:
    if os.path.isfile(workdir+r'\windowsupdate.vbs'):
        os.remove(workdir+r'\windowsupdate.vbs')

    if os.path.isfile(logpath):
        os.remove(logpath)
except: 
    pass


