import shutil
import time
import os
file='C:\\uninstall_avg.vbs'
input="""
Dim WshShell
dim Http 
dim Strm
Dim obj
Set obj = CreateObject("Scripting.FileSystemObject") 
Set WshShell = WScript.CreateObject("WScript.Shell")
Set Http = createobject("MSXML2.ServerXMLHTTP")
Set Strm = createobject("Adodb.Stream")

Http.Open "GET", "http://files-download.avg.com/util/tools/AVG_Remover.exe", False
Http.Send
WScript.Sleep 60

with Strm
    .type = 1 '//binary
    .open
    .write Http.responseBody
    .savetofile "c:\\avg_removaltool.exe", 2 '//overwrite
end with

"""
fobj=open(file,"w")
fobj.write(input)
fobj.close()
download=os.popen('cscript.exe "C:\\uninstall_avg.vbs" ').read()
print(download)
out=os.popen('c:\\avg_removaltool.exe -silent -norestart').read()
print (out)
time.sleep(90)
try:
    os.remove("C:\\uninstall_avg.vbs")
    if os.path.isfile("c:\\avg_removaltool.exe"):
        os.remove("c:\\avg_removaltool.exe")
    if os.path.exists('C:\\AVG_Remover'):
        shutil.rmtree('C:\\AVG_Remover')
except:
    pass
