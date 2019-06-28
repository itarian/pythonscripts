sitelist = "www.google.com,www.gmail.com,www.youtube.com"
 
 
import os
import ctypes
drive=os.environ['SYSTEMDRIVE']
users=drive+'\\Users'

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
 
    lines='''
    Dim list
    Dim urlnames
     
    list = "%s"
    urlnames=Split(list,",")
    Set obj = CreateObject("Scripting.FileSystemObject")
     
    For i = 0 to UBound(urlnames) 
      website=urlnames(i)
      name=Split(urlnames(i),".")
      url=name(1)
      deletebookmark  url
      addbookmark website,url 
    Next
     
     
     
    Sub addbookmark(website,url)
        Set objShell = WScript.CreateObject("WScript.Shell")
        allUsersDesktop = objShell.SpecialFolders("AllUsersDesktop")
        usersDesktop = objShell.SpecialFolders("Desktop")
        Set objShortCut = objShell.CreateShortcut(allUsersDesktop & "/" & url & ".url")
        objShortCut.TargetPath = website
        objShortCut.Save
            WScript.Echo website & "-------"& "Bookmark for this website saved in desktop as  "&url
    End Sub
     
    Sub deletebookmark(url)
        on error resume next
        Set Shell = CreateObject("WScript.Shell")
        Set FSO = CreateObject("Scripting.FileSystemObject")
        allUsersDesktop = Shell.SpecialFolders("AllUsersDesktop")     
        FSO.DeleteFile allUsersDesktop & "\"& url & ".url"   
    End Sub
     
     
     
     
    '''
    vblines=lines % (sitelist)
     
    temp=os.environ['TEMP']
    path=temp+'\\desktopbookmark.vbs'
     
     
    files=open(path,'w+')
    files.write(vblines)
    files.close()
     
    os.chdir(temp)
     
    if 'PROGRAMW6432' in os.environ.keys():
        result=os.popen(r'C:\Windows\SysWOW64\cscript.exe desktopbookmark.vbs').read()
        print result
    else:
        result=os.popen(r'C:\Windows\System32\cscript.exe desktopbookmark.vbs').read()
        print result
     
     
     
    userlist=[]
     
    for i in os.listdir(users):   
        if (('Default' in i) or ('Public' in i) or ('desktop' in i) or 'All Users' in i):       
            pass
        else:
            userlist.append(users+'\\'+i+"\\Desktop")
     
     
    for i in userlist:   
        if os.path.exists(i):       
            print 'URL bookmarks added to  "'+i+'" '
     
     
    try:
        os.remove(path)
    except:
        pass

