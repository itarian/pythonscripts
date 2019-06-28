file_name=r"**************************"#user need to give the file name(eg:itsm_gPB4RS3N_installer.msi)
run_as_username=r'*******'#Please edit with your system username
run_as_password=r'******'#Please edit with your system password
task_name=r'ComodoInstall'
task_run=r'C:\\ProgramData\\ComodoInstall.bat'
import ctypes
import os
import re
import subprocess
src_path=r'C:\temp\ComodoInstalls'##  Here mention the path where the application to download
dest_path=src_path+"//"+"log.txt"

if not os.path.exists(src_path):
    os.makedirs(src_path)
URL='http://dl.cmdm.comodo.com/download/COCC.msi' ## Here mention the download Link
a=0
b=0

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def Download(src_path, URL):
    import urllib2
    import os
    print file_name+"...Download started"
    fileName = file_name
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if not os.path.exists(src_path):
        os.makedirs(src_path)
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    print file_name+"..Download completed"
    return fp

down_path=Download(src_path, URL)
#to uninstall rmm agent
k=[];
with disable_file_system_redirection():
    guid=os.popen(r"wmic product get name,identifyingnumber").read();
    k.append(re.findall("{.*",guid));
j=[];
for i in k[0]:
	j.append(i);
rmm=re.findall("RMM Agent Service",guid);
if rmm:
    with disable_file_system_redirection():
        os.popen(r'wmic product where name="RMM Agent Service" call uninstall').read()
        print " RMM Agent Service is  uninstalled on Endpoint"
        with open(dest_path,"wb") as e:
            e.write("RMM Agent Service: FOUND, REMOVED\n")
else:
    print('RMM Agent is not installed at Endpoint');
    with open(dest_path,"wb") as f:
        f.write("RMM Agent Service:  NOT FOUND, N\A\n")
###########to uninstall pm agent
        
def uninstall (find):
    with disable_file_system_redirection():
        command='wmic product where name="Comodo One Patch Management Agent" call uninstall'
        uninst=os.popen(command).read()
    return command
def check():
    with disable_file_system_redirection():
        inst=os.popen("wmic product get name,identifyingnumber").read()
    return inst
inst=check()
 
if len(inst)>0:
    find=re.findall('{.*}\s\sComodo\sOne\sPatch\sManagement\sAgent',inst)
    if len(find)>0:
        final=re.findall('{.*}',find[0])[0]
        if len(final) >0:
            a=1
if a ==1:
    print "Comodo One Patch Management Agent is  installed on Endpoint"
    if uninstall(find):
        print " Comodo One Patch Management Agent is  uninstalled on Endpoint"
        with open(dest_path,"a+") as f:
            f.write("\nComodo One Patch Management Agent: FOUND, REMOVED\n")
else:
    print "Comodo One Patch Management Agent is  not installed on Endpoint"
    with open(dest_path,"a+") as f:
        f.write("\nComodo One Patch Management Agent:  NOT FOUND, N\A\n")
    
###########to uninstall ccs
        
blacklist=['COMODO Client - Security']
def ecmd(CMD, OUT=False):
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    ret=OBJ.returncode
    return ret

def collectprograms(rtkey,pK,kA):
    import _winreg
    import os
    list=[]
    oK=_winreg.OpenKey(rtkey,pK,0,kA)
    i=0
    while True:
        try:
            bkey=_winreg.EnumKey(oK,i)
            vkey=os.path.join(pK,bkey)
            oK1=_winreg.OpenKey(rtkey,vkey,0,kA)
            try:
                DN,bla=_winreg.QueryValueEx(oK1,'DisplayName')
                DV,bla=_winreg.QueryValueEx(oK1,'DisplayVersion')
                inlist=[DN.strip(), DV.strip()]                    
                try:
                    IL, bla=_winreg.QueryValueEx(oK1,'InstallLocation')
                    if not IL:
                        IL='none'
                except:
                    IL='none'
                if IL:
                    inlist.append(IL.strip())
                else:
                    inlist.append(IL)
                try:
                    US,bla=_winreg.QueryValueEx(oK1,'UninstallString')
                except:
                    US='none'
                if US:
                    inlist.append(US.strip())
                else:
                    inlist.append(US)
                try:
                    QS,bla=_winreg.QueryValueEx(oK1,'QuietUninstallString')
                    if QS:
                        inlist.append(QS.strip())
                except:
                    pass
                list.append(inlist)
                _winreg.CloseKey(oK1)
            except:
                pass
            i+=1
        except:
            break
    _winreg.CloseKey(oK)
    return list

import os
import _winreg
uninstallkey='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
if 'PROGRAMFILES(X86)' in os.environ.keys():
    rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
            (_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ),
            (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
            (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ)]
else:
    rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_READ),
            (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_READ)]
collected=''
uninstalled=''
error=''
blacklisted=''
hasnoss=[]
ic=0
uc=0
ec=0
for i in rklist:
    col=collectprograms(i[0], i[1], i[2])    
    for c in col:
        citer='|'.join(c)
        if citer not in collected:                
            if c[0].lower() in [b.lower() for b in blacklist]:
                if len(c)>4:
                    blacklisted+='%d %s == %s\n'%(ic+1, c[0], c[1])
                    us=ecmd(c[4])
                    if us==0:
                        uninstalled+='%d %s == %s\n'%(uc+1, c[0], c[1])
                        uc+=1
                    else:
                        error+='%d %s == %s - error code %d\n'%(ec+1, c[0], c[1], us)
                        ec+=1
                    ic+=1
                else:
                    blacklisted+='%d %s == %s\n'%(ic+1, c[0], c[1])
                    if c[3].startswith('MsiExec.exe'):
                        us=ecmd(c[3].replace('MsiExec.exe /I', 'MsiExec.exe /X')+' /qn'+' /norestart')
                        if us==0:
                            uninstalled+='%d %s == %s\n'%(uc+1, c[0], c[1])
                            uc+=1
                        elif us==3010:
                            uninstalled+='%d %s == %s\n'%(uc+1, c[0], c[1])
                            print 'System restarts required for the changes to take affect'
                            uc+=1
                        else:
                            error+='%d %s == %s - error code %d\n'%(ec+1, c[0], c[1], us)
                            ec+=1
                    else:
                        hasnoss.append('%s\n'%(citer))
                    ic+=1
            collected+=citer+'\n'
if blacklisted:
    if uninstalled:
        print '\nCOMODO CLIENT SECURITY is removed successfully: \n', uninstalled
        with open(dest_path,"a+") as f1:
            f1.write("COMODO CLIENT SECURITY: FOUND, REMOVED")   
    if error:
        print '\nerror at removing the COMODO CLIENT SECURITY: \n', error
else:
    print 'COMODO CLIENT SECURITY is not installed on endpoint'
    with open(dest_path,"a+") as f1:
        f1.write("\nCOMODO CLIENT SECURITY: NOTFOUND, N/A\n")                 
    if blacklist:
        c=0
        for i in blacklist:
            if i==blacklist[-1]:
                c+=1
            else:
                c+=1

            
#to create bat file
BAT=r'''msiexec /i %s\%s /qn'''%(src_path,file_name)
bat_path=os.environ['programdata']+"\ComodoInstall.bat"
with open(bat_path,"w") as f:
    f.write(BAT)
    
# schedule task 
def del_task_schedule():
    with disable_file_system_redirection():
        process1=os.popen("schtasks /query").read()
        if "ComodoInstall" in process1:
            process2= subprocess.Popen('schtasks /delete /tn "%s" /f'%(task_name), shell=True, stdout=subprocess.PIPE)
            result=process2.communicate()
            ret=process2.returncode
def task_schedule():
    process= subprocess.Popen('schtasks /create /ru "%s" /rp "%s" /sc "ONSTART" /tn "%s" /tr "%s" /f'%(run_as_username, run_as_password, task_name, task_run), shell=True, stdout=subprocess.PIPE)
    result=process.communicate()
    ret=process.returncode
del_task_schedule()
task_schedule()

#to uninstall ccc
def uninstall_ccc():
    with disable_file_system_redirection():
        command='wmic product where name="COMODO Client - Communication" call uninstall'
        command1='wmic product where name="COMODO Client - Communication Updater" call uninstall'
        uninst=os.popen(command).read()
        uninst1=os.popen(command1).read()
def check():
    with disable_file_system_redirection():
        inst1=os.popen("wmic product get name,identifyingnumber").read()
    return inst1
inst1=check()
 
if len(inst1)>0:
    find=re.findall('{.*}\s\sCOMODO\sClient\s-\sCommunication',inst1)
    if len(find)>0:
        final=re.findall('{.*}',find[0])[0]
        if len(final) >0:
            a=1
    find1=re.findall('{.*}\s\sCOMODO\sClient\s-\sCommunication\sUpdater',inst1)
    if len(find1)>0:
        final1=re.findall('{.*}',find1[0])[0]
        if len(final1) >0:
            a=1
if a==1:
    uninstall_ccc()
    print " COMODO Client - Communication  is  uninstalled on Endpoint"
    with open(dest_path,"a+") as f2:
        f2.write("COMODO Client - Communication: FOUND, REMOVED\n")
else:
    print "COMODO Client - Communication  is  not installed on Endpoint"
    with open(dest_path,"a+") as f2:
        f2.write("COMODO Client - Communication:  NOT FOUND, N\A\n")             
