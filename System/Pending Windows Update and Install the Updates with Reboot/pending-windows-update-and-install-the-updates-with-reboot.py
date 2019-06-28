import os
import re
import ctypes
import time
import subprocess
from subprocess import PIPE, Popen

a=0
def install_update():
    vbs=r'''
    var=%s
    Set updateSession = CreateObject("Microsoft.Update.Session")
    updateSession.ClientApplicationID = "MSDN Sample Script"

    Set updateSearcher = updateSession.CreateUpdateSearcher()

    WScript.Echo "Searching for updates..." & vbCRLF

    Set searchResult = _
    updateSearcher.Search("IsInstalled=0 and Type='Software' and IsHidden=0")

    WScript.Echo "List of applicable items on the machine:"

    For I = 0 To searchResult.Updates.Count-1
        Set update = searchResult.Updates.Item(I)
        WScript.Echo I + 1 & "> " & update.Title
    Next

    If searchResult.Updates.Count = 0 Then
        WScript.Echo "There are no applicable updates."
        WScript.Quit
    End If

    WScript.Echo vbCRLF & "Creating collection of updates to download:"

    Set updatesToDownload = CreateObject("Microsoft.Update.UpdateColl")

    For I = 0 to searchResult.Updates.Count-1
        Set update = searchResult.Updates.Item(I)
        addThisUpdate = false
        If update.InstallationBehavior.CanRequestUserInput = true Then
            WScript.Echo I + 1 & "> skipping: " & update.Title & _
            " because it requires user input"
        Else
            If update.EulaAccepted = false Then
                WScript.Echo I + 1 & "> note: " & update.Title & _
                " has a license agreement that must be accepted:"
                WScript.Echo update.EulaText
                WScript.Echo "Do you accept this license agreement? (Y/N)"
                strInput = WScript.StdIn.Readline
                WScript.Echo 
                If (strInput = "Y" or strInput = "y") Then
                    update.AcceptEula()
                    addThisUpdate = true
                Else
                    WScript.Echo I + 1 & "> skipping: " & update.Title & _
                    " because the license agreement was declined"
                End If
            Else
                addThisUpdate = true
            End If
        End If
        If addThisUpdate = true Then
            WScript.Echo I + 1 & "> adding: " & update.Title 
            updatesToDownload.Add(update)
        End If
    Next

    If updatesToDownload.Count = 0 Then
        WScript.Echo "All applicable updates were skipped."
        WScript.Quit
    End If
        
    WScript.Echo vbCRLF & "Downloading updates..."

    Set downloader = updateSession.CreateUpdateDownloader() 
    downloader.Updates = updatesToDownload
    downloader.Download()

    Set updatesToInstall = CreateObject("Microsoft.Update.UpdateColl")

    rebootMayBeRequired = false

    WScript.Echo vbCRLF & "Successfully downloaded updates:"

    For I = 0 To searchResult.Updates.Count-1
        set update = searchResult.Updates.Item(I)
        If update.IsDownloaded = true Then
            WScript.Echo I + 1 & "> " & update.Title 
            updatesToInstall.Add(update) 
            If update.InstallationBehavior.RebootBehavior > 0 Then
                rebootMayBeRequired = true
            End If
        End If
    Next

    If updatesToInstall.Count = 0 Then
        WScript.Echo "No updates were successfully downloaded."
        WScript.Quit
    End If

    If rebootMayBeRequired = true Then
        WScript.Echo vbCRLF & "These updates may require a reboot."
    End If

    WScript.Echo  vbCRLF & "installing updates now"
    strInput = "Y"
    WScript.Echo 

    If (strInput = "Y" or strInput = "y") Then
        var=1
        WScript.Echo "Installing updates..."
        WScript.Echo "Variable"&var
        Set installer = updateSession.CreateUpdateInstaller()
        installer.Updates = updatesToInstall
        Set installationResult = installer.Install()
     
        'Output results of install
        WScript.Echo "Installation Result: " & _
        installationResult.ResultCode 
        WScript.Echo "Reboot Required: " & _ 
        installationResult.RebootRequired & vbCRLF 
        WScript.Echo "Listing of updates installed " & _
        "and individual installation results:" 
     
        For I = 0 to updatesToInstall.Count - 1
            WScript.Echo I + 1 & "> " & _
            updatesToInstall.Item(i).Title & _
            ": " & installationResult.GetUpdateResult(i).ResultCode   
        Next
    End If
        
    ''' %(a)

    try:
        workdir=os.environ['PROGRAMDATA']+r'\temp'
        if not os.path.exists(workdir):
            os.mkdir(workdir)      
    except:
        workdir=os.environ['SYTEMDRIVE']


        
    
    script =vbs

    with open(workdir+r'\windowsupdate.vbs',"wb") as f :
        f.write(script)
        


    obj = subprocess.Popen('cscript.exe "'+workdir+'\windowsupdate.vbs"', shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    print out
    p=re.findall("Variable(.*)",out)
    print p

    if p==['1\r']:
        print "System is restarting...."
        os.popen("shutdown -r -t 0").read()
    else:
        pass

    try:
        if os.path.isfile(workdir+r'\windowsupdate.vbs'):
            os.remove(workdir+r'\windowsupdate.vbs')

    except: 
        pass

install_update()


