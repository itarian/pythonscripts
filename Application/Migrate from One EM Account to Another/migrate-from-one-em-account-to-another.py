host=itsm.getParameter("Enter_the_Host_name")           #please provide the host of new EM portal 
port=itsm.getParameter("Enter_the__port_name")      #please provide the port of new EM portal
token=itsm.getParameter("Enter_the_Token")        #please provide the token of new EM portal 

import os
import time
drive=os.environ['SystemDrive']

enrollment='''[General]
host = %s
port = %s
remove_third_party = false
suite = 4
token = %s
'''%(host,port,token)

unenrollment=''':CheckOS
IF EXIST "%PROGRAMFILES(X86)%" (GOTO 64BIT) ELSE (GOTO 32BIT)

:64BIT
cd "%ProgramFiles(x86)%\COMODO\Comodo ITSM"
ITSMService.exe -c 2
GOTO END

:32BIT
cd "%ProgramFiles%\COMODO\Comodo ITSM"
ITSMService.exe -c 2
GOTO END

:END
timeout 10'''

restart='''@ECHO OFF

NET STOP ITSMservice

TIMEOUT /t 10 /NOBREAK

NET START ITSMservice

EXIT'''



def unenroll():
    path=os.environ['programdata']+"\unenroll.bat"
    with open(path,"w") as f:
        f.write(unenrollment)
    cmd=os.popen(path).read()
    time.sleep(30)
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass

def config():
    if os.path.exists(drive+"\Program Files (x86)"):
        path1=drive+"\Program Files (x86)\COMODO\Comodo ITSM\enrollment_config.ini"
        with open(path1,"w") as a:
            a.write(enrollment)
    else:
        path1=drive+"\Program Files\COMODO\Comodo ITSM\enrollment_config.ini"
        with open(path1,"w") as b:
            b.write(enrollment)
    path2=os.environ['programdata']+"\service.bat"
    with open(path2,"w") as c:
        c.write(restart)
    print "ITarian communication client will be enrolled to new EndPoint Manager portal "
    cmd2=os.popen(path2).read()
    time.sleep(30)
    if os.path.exists(path2):
        try:
            os.remove(path2)
        except:
            pass
    
    


print "Unenrolling ITarian communication client from old EndPoint Manager portal..."
unenroll()
print "configuring new EndPoint Manager details"
config()
