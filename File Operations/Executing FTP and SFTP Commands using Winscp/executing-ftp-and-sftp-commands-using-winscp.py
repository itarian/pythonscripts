
#store all ftp commands one by one as in below 

instruction="""

open ftp://usernameassword@hostname.com:/ -hostkey=* 
put "C:\Users\test\Documents\sample.zip"
close
exit

""" 
path1=r'C:\Program Files (x86)\WinSCP' # Winscp File path
import os
import ctypes
from subprocess import PIPE, Popen

Path=os.environ['temp'] 
 
os.chdir(Path)
from subprocess import PIPE, Popen
with open('run.txt',"w+") as obj:
    obj.write(instruction)
    obj.close()
 
    os.chdir(Path)
    
    transfer_object=Popen((r'"%s\WinSCP.exe" /script=run.txt'%path1), shell=True, stdout=PIPE, stderr=PIPE)
    transfer_object.communicate()
    ki=transfer_object.returncode
    if ki==0:
        print ("The File FTP upload completed successfully!")
    else:
        print("No File uploaded")

try:
    os.remove(path)
except:
    pass
    
    
