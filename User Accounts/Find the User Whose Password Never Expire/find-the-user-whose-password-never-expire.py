import os
import re
powershell =r'''
Import-Module ActiveDirectory
get-aduser -filter * -properties Name, PasswordNeverExpires | where { $_.passwordNeverExpires -eq "true" }
'''
file_name='powershell_file.ps1'
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(powershell)
sm=os.popen('powershell "Set-ExecutionPolicy RemoteSigned"').read()
cmd1=os.popen('powershell "%s"'%file_path).read()
if cmd1:
    a=cmd1.split(',')
    c=''.join(a)
    b=re.findall("DistinguishedName    : CN=(.*)", c)
    print("---------The password never expires for the following users----------------- ")
    for i in b:
        d= re.findall("(.*)CN=",i)
        d1=''.join(d)
        print d1 
else:
    print("There are no users available whose password never expire")



