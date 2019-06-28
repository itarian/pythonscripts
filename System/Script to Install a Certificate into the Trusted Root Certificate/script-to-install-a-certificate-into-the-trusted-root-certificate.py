
path="C:\Users\DUKE\Desktop" # Give the certificate path
filename="bob.crt" #Give the certificate name with extension


import os
import subprocess

cmd=os.path.join(path,filename)

cmd1=r'CERTUTIL -addstore -enterprise -f -v root "%s"'%cmd

process= subprocess.Popen(cmd1,shell=True, stdout=subprocess.PIPE)
result=process.communicate()
print result
ret=process.returncode

if ret==0:
    print filename+" is installed to trusted root certificate succesfully"
    
else:
    print filename+" is not installed to trusted root certificate"
       
        
