KB="KB3127220"   # Enter the KB value of patch which you want to install.


import os
import re
import ctypes
import time
import subprocess
from subprocess import PIPE, Popen


def install_update():
    import os

    vbs=r'''
    KB="%s"
    j=0
    Set updateSession = CreateObject("Microsoft.Update.Session")

    Set updateSearcher = updateSession.CreateUpdateSearcher()
    Set updateDownloader = updateSession.CreateUpdateDownloader()
    Set updateInstaller = updateSession.CreateUpdateInstaller()
    Sub test()
        WScript.Echo "Came inside the function"
    End Sub

    Do

      WScript.Echo
      WScript.Echo "Searching for approved updates ..."
      WScript.Echo

      Set updateSearch = updateSearcher.Search("IsInstalled=0")

      If updateSearch.ResultCode <> 2 Then

        WScript.Echo "Search failed with result code", updateSearch.ResultCode
        WScript.Quit 1

      End If

      If updateSearch.Updates.Count = 0 Then

        WScript.Echo "There are no updates to install."
        WScript.Quit 2

      End If

      Set updateList = updateSearch.Updates

      For I = 0 to updateSearch.Updates.Count - 1

        Set update = updateList.Item(I)

        WScript.Echo "Update found:", update.Title

      Next

      WScript.Echo

      
      Set updateToInstall = CreateObject("Microsoft.Update.UpdateColl")
      For I = 0 to updateList.Count - 1
        
        If InStr(1, updateList.Item(I).Title, KB) > 0 Then
         j=1
         WScript.Echo "Selected  update " & updateList.Item(I).Title
         updateToInstall.Add(updateList.Item(I))
         'Download update
         Set downloader = updateSession.CreateUpdateDownloader() 
         downloader.Updates = updateToInstall
         WScript.Echo vbCRLF & "Downloading..."
         
         Set downloadResult = downloader.Download()
         
         WScript.Echo "Download Result: " & downloadResult.ResultCode
         test()
      
         'Install Update
         Set installer = updateSession.CreateUpdateInstaller()
         WScript.Echo vbCRLF & "Installing..."
         installer.Updates = updateToInstall
         Set installationResult = installer.Install()
      
         'Output the result of the installation
         WScript.Echo "Installation Result: " & _
         installationResult.ResultCode
         WScript.Echo "Reboot Required: " & _
         installationResult.RebootRequired 
        
        End If
     Next
     If j=0 Then
     WScript.Echo "Selected KB value is not available in Update list. Please give applicable KB value"
     WScript.Quit 0
     End If 
     Loop
    '''

    try:
        workdir=os.environ['PROGRAMDATA']+r'\temp'
        if not os.path.exists(workdir):
            os.mkdir(workdir)      
    except:
        workdir=os.environ['SYTEMDRIVE']


        
    
    script =vbs % (KB)

    with open(workdir+r'\windowsupdate.vbs',"wb") as f :
        f.write(script)        


    obj = subprocess.Popen('cscript.exe "'+workdir+'\windowsupdate.vbs"', shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    print out

    try:
        if os.path.isfile(workdir+r'\windowsupdate.vbs'):
            os.remove(workdir+r'\windowsupdate.vbs')

    except: 
        pass

install_update()
