import os
vbs='''
Dim objShell
Set objShell = WScript.CreateObject( "WScript.Shell" )
objShell.Run "taskkill /im TeamViewer.exe", , True
objShell.Run("""%ProgramFiles%\TeamViewer\uninstall.exe"" /S")
Set objShell = Nothing
'''

path=os.environ['TEMP']
drive=os.environ['SYSTEMDRIVE']
filepath=path+'\\removetv.vbs'
fob=open(filepath,'w+')
fob.write(vbs)
fob.close()

if 'PROGRAMW6432' in  os.environ.keys():
    out=os.popen(drive+'\\Windows\\SysWOW64\\cscript.exe   '+filepath).read()
    print (out)
else:
    out=os.popen(drive+'\\Windows\\system32\\cscript.exe   '+filepath).read()
    print (out)

try:
    os.remove(filepath)
except:
    pass

print ('Team viewer uninstalled successfully')