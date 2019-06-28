Dest=r'*****************'  # provide the Destination share path
share_user="******"  # provide the  share path user name 
share_pass="********" #provide the  share path password
import os,codecs,time,ctypes
user=os.popen("wmic useraccount get name").read()
l=[user]
m=l[0].split()
username=[]
for z in m:
    if 'Name' in z or 'Administrator' in z or 'DefaultAccount' in z or 'Guest' in z:
        pass
    else:
        username.append(z)
des_fname=r"cobian_backup_folder"
drive=os.environ['SYSTEMDRIVE']
source=[]
for i in username:
    Source1="%s\Users\%s\Documents"%(drive,i)
    Source2="%s\Users\%s\Desktop"%(drive,i)
    source.append(Source1)
    source.append(Source2)
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
cnd='NET USE "'+Dest+'" /USER:'+share_user+'  "'+share_pass+'"'
Destination=Dest+'\\'+des_fname
print 'Login to network share'
with disable_file_system_redirection():
    print os.popen(cnd).read()

line=""
a="1"
g=[]
for i in range(len(source)):
    c=tuple([a]+[source[i]])
    g.append(c)
    

te=''
ke=[]
s=''
for i in range(len(g)):
    s += "(" + ', '.join(map(str,g[i])) + ")"



te=s.replace("(",'"')

ge=te.replace(")",'"')

ve=ge.replace('""','","')

st=''
line='Source='+ve


multistring='''{11//
Id={FA5A98F3-A92B-476B-B437-CA06EF697BFD}
Name=New task
Group=
Enabled=true
Include subdirectories=true
Create separated backups=true
Use attributes=true
Use VSC=true
Backup type=0
Priority=0
%s
Destination="1,%s"
Schedule type=1
Select days of the week=false
 Order of Day of the week=1
Day of the week=1
Date/Time=0100000011100101000101100110010100000011010110010010001101011000
Day of the month=1
Month=1
Timer=180
Timer from=0100000011100101000101100110000000000000000000000000000000000000
Timer to=0100000011100101000101100111111111111111111001111011101000110111
Full copies=0
Differental copies=0
One full every=0
Use fixed day=false
Fixed day=1
Compression=0
Compress individually=false
Split=0
Custom size=4300000000
Comment=Cobian Backup 11 Gravity
Encryption=0
Passphrase=cwBzAHkAfAB+AGcAdQBuAHYAdQArAGEAFAADABcAcwB8AHUAfwAdABMAcgB/AHIAZQAEABYAAABrAB0AbwAJAHsAdwBmACwAFgABAG8ADAB1AAoAcAB/AHgAdgAOACQAZAAoAA==
Exclusions=
Inclusions=
Pre backup events=
Post backup events=
Abort if pre-event fails=false
Abort if post-event fails=false
Mirror=false
Absolute paths=false
Always create top directory=true
Clear archive attribute=true
Include backup type=true
Delete empty directories=false
Impersonate=false
Abort if impersonation fails=false
Run as User name=
Run as Domain=.
Run as Password=cgB/AHoAeQByAHgAZwB2AHQAbQAsAHcAEwADAAMAcwBuAHUAeAAdAAEAcgBxAHIAdAAEAAUAAABhAB0AaAAJAHkAdwB4ACwADQABAHEABwBwAAwAeQB1AGUAdQAQADkAewAqAA==
//11}'''%(line,Destination)


if os.path.exists("C:\Program Files (x86)"):
    path="C:\Program Files (x86)\Cobian Backup 11\DB\list.lst"
    directory="C:\Program Files (x86)\Cobian Backup 11"
else:
    path="C:\Program Files\Cobian Backup 11\DB\list.lst"
    directory="C:\Program Files\Cobian Backup 11"

def stopservice():
    task=os.popen('tasklist"').read()
    try:
        if "Cobian.exe" in task:
            service=os.popen('Tasklist |Findstr "Cobian.exe"').read()
            stop=os.popen('Taskkill /IM Cobian.exe /F').read()
        else:
            pass
    except:
        pass
        
    
with codecs.open(path, mode='w', encoding='utf-16-le') as f:
        f.write(multistring)


stopservice()
os.chdir(directory)
time.sleep(20)
CMD='Cobian.exe "-list:%s" -nogui -bu -autoclose'%path
sample=os.popen(CMD).read()

print "Copied successfully....."
print "Check your copied data's in the path " +Destination
