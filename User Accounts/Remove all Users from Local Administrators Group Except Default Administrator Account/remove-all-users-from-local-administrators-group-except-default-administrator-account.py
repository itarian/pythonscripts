import os
temp=os.environ['TEMP']

vbs=r'''
Set WshShell = WScript.CreateObject("WScript.Shell")
Set colItems = GetObject("winmgmts:\\.\root\cimv2").ExecQuery("Select * from Win32_UserAccount Where LocalAccount=True")

On Error Resume Next
For Each objItem in colItems
    If objItem.Name <> "Administrator" Then
        cmd="net localgroup administrators  """ & objItem.Name & """   /delete"        
        WshShell.Run cmd,0, True
        WScript.Echo  objItem.Name & "  removed from local administrator group"
    End If
Next

'''

with open(temp+r'\remove_admin.vbs',"wb") as f :
    f.write(vbs)        

os.chdir(temp)

if 'PROGRAMW6432' in os.environ.keys():
    vb=os.environ['SYSTEMROOT']+r'\SysWOW64\cscript.exe'
    print os.popen(vb+'    remove_admin.vbs').read()
else:
    vb=os.environ['SYSTEMROOT']+r'\System32\cscript.exe'
    print os.popen(vb+'    remove_admin.vbs').read()


if os.path.isfile('remove_admin.vbs'):
    os.remove('remove_admin.vbs')
