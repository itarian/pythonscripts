import os
import re
start_services=[]
stop_services=[]
restart_services=[]
pause_services=[]
resume_services=[]
serv_demand=[]
serv_disabled=[]
startup_dele=[]
ex={}
##start_services=['BDESVC']
##stop_services=['DPS',''MSDT'']
##restart_services=['WPCSvc']
##pause_services=['MSDT']
##resume_services=['gpsvc ']
##serv_demand=['vmicrdv']
##serv_disabled=['WlanSvc']
##startup_dele=['CCleaner']
##ex={"Google Chrome":"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe","CCleaner":"C:\Program Files\CCleaner\CCleaner.exe"}

def ecmd(CMD, r=False):
    import ctypes
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    ret=OBJ.returncode
    if r:
        return ret
    else:            
        if ret==0:
            return out,ret
        else:
            return err,ret
ps_command='Get-Service | Sort-Object displayname'
import subprocess
import ctypes

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
    process=subprocess.Popen('powershell "%s"'%ps_command, shell=True, stdout=subprocess.PIPE)
result=process.communicate()
ret=process.returncode
if ret==0:
    if result[0]:
        fin=result[0].strip()
    else:
        print None
        
else:
    print '%s\n%s'%(str(ret), str(result[1]))
print '\n'
print '\t'+'LIST OF ALL SERIVES WHICH ARE RUNNING IN YOUR SYSTEM'
print fin
print '\n'
print 'LIST OF STARTUP PROGREAMS WICH ARE RUNNING IN YOUR SYSTEM'
startup=os.popen('wmic startup get caption ').read()
print startup
print '\n'



#start services
def start_ser():
    if len(start_services)!=0:
        for i in range(0,len(start_services)):
            cmd1,ret1=ecmd('net start %s'%start_services[i])
            if ret1!=0:
                qu=os.popen('sc queryex %s'%start_services[i]).read()
                reg=re.findall('(PID.*)',qu)
                st1=' '.join(reg)
                fin =st1.split(':')[1]
                g=os.popen('taskkill /pid:%s /F'%fin).read()
                cmd_start,rt=ecmd('net start %s'%start_services[i])
                print 'AFTER PROCESSING...........................'
                print cmd_start
            else:
                print cmd1
start_ser()

def stop_ser():
    if len(stop_services)!=0:
    #stop particluar services.     
        for j in range(0,len(stop_services)):
            cmd2,ret2=ecmd('net stop %s'%stop_services[j])
            if ret2!=0:
                qu2=os.popen('sc queryex %s'%stop_services[j]).read()
                reg2=re.findall('(PID.*)',qu2)
                st2=' '.join(reg2)
                fin2 =st2.split(':')[1]
                g2=os.popen('taskkill /pid:%s /F'%fin2).read()
                cmd_start2,rt2=ecmd('net stop %s'%stop_services[j])
                print 'AFTER PROCESSING................................... '
                print cmd_start2
            else:
                print cmd2
stop_ser()

def restart_ser():
    if len(restart_services)!=0:
    #Restart services.
        for h in range(0,len(restart_services)):
            res,ret8=ecmd('net stop %s'%restart_services[h])
            if ret8!=0:
                qu3=os.popen('sc queryex %s'%restart_services[h]).read()
                reg3=re.findall('(PID.*)',qu3)
                st3=' '.join(reg3)
                fin3 =st3.split(':')[1]
                g3=os.popen('taskkill /pid:%s /F'%fin3).read()
                cmd_start3=os.popen('net stop %s'%restart_services[h]).read()
                res22,ret9=ecmd('net start %s'%restart_services[h])
                print 'SERVICES HAS BEEN RESTARTED ......'+ restart_services[h]
            else:
                res23,ret9=ecmd('net start %s'%restart_services[h])
                print 'A '+ restart_services[h]+'  SERVICE  HAS BEEN RESTARTED ......    '
        print '\n'
restart_ser()

def pause_ser():
    if len(pause_services)!=0:
        #pause
        for p in range(0,len(pause_services)):
            pause,ret11=ecmd('net pause %s'%pause_services[p])
            if ret11!=0:
                print 'Unable to pause the service....  '+ pause_services[p]
            else:
                print 'A  '+pause_services[p]+ '  has been paused'
        print '\n'
pause_ser()


def resume_ser():
    if len(resume_services)!=0:
    #resume
        for e in range(0,len(resume_services)):
            resume,ret33=ecmd('net continue %s'%resume_services[e])
            if ret33!=0:
                print 'Unable to resume the service....  '+ resume_services[e]
            else:
                print 'A  '+resume_services[e]+ '  has been resumed'
        print '\n'
resume_ser()


def disable_ser():
    if len(serv_disabled)!=0:
        #service on disabled
        for u in range(0,len(serv_disabled)):
            dis,retdis=ecmd('sc config %s start=disabled'%serv_disabled[u])
            if retdis!=0:
                print 'UNABLE TO DISABLED THE SERVICE'
            else:
                print serv_disabled[u]+' '+dis
        print '\n'
disable_ser()



def demand_ser():
    if len(serv_demand)!=0:
    #service on demand
        for w in range(0,len(serv_demand)):
            dem,retdem=ecmd('sc config %s start=demand'%serv_demand[w])
            if retdem!=0:
                print 'FAILED TO DEMAND THE SERVICE'
            else:
                print serv_demand[w]+' '+ dem
        print '\n'
demand_ser()


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
pa=[]
soft_names=[]
soft_location=[]
soft_file=[]
ic=0
a=[]
uc=0
ec=0
for i in rklist:
    col=collectprograms(i[0], i[1], i[2])
    a.append(col)
    
for j in range(0,len(a[0])):
    pa.append(a[0][j])
for l in range(0,len(a[1])):
    pa.append(a[1][l])

print '***LIST OF PROGRAMS PRESENT IN YOUR SYSTEM***'
for u in range(0,len(pa)):
    soft_names.append(pa[u][0])
for e in range(0,len(soft_names)):
    print soft_names[e]
print '\n'

def my_pro(name,path):
    if len(ex)!=0:
        import unicodedata
        tx=os.popen('reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\\ /s').read()
        if name in tx:
            print name+' ALREADY EXISTS IN STARTUP PROGRAMS'
        else:  
            for k in range(0,len(pa)):
                if name in pa[k]:
                    soft_location=unicodedata.normalize('NFKD',pa[k][2]).encode('ascii','ignore')
                    soft_file=unicodedata.normalize('NFKD',pa[k][3]).encode('ascii','ignore')
                    
            if os.path.exists(soft_location):
                if os.path.isfile(path):
                    g,ret_reg=ecmd('reg  add  HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\ /v '+'"'+name+'"'+' /t REG_EXPAND_SZ /d "%s"'%path)
                    print 'Sucessfully added '+name +' to startup programs.'
                else:
                    print 'please give correct path'
            else:
                print 'Given location not exists'
for i in range(0,len(ex)):
     my_pro(ex.keys()[i],ex.values()[i])
def startup_delete():
    if len(startup_dele)!=0:
    #remove startup prgrams formthe list
        print '\n'
        for k in range(0,len(startup_dele)):
            start_up,ret3=ecmd('wmic startup where caption="%s" list full'%startup_dele[k])
            start_up_reg=re.findall('Location=(.*)',start_up)
            v=' '.join(start_up_reg)
            x=v.strip('\\r')
            #operations
            if x.startswith('HKU'):
                x_fin=ecmd('reg delete '+ x.replace('HKU',' HKEY_USERS')+' '+'/v'+' '+'"%s" /f   '%startup_dele[k])
            elif x.startswith('HKLM'):
                x_fin=ecmd('reg delete '+ x.replace('HKLM','HKEY_LOCAL_MACHINE')+' '+'/v'+' '+'"%s" /f   '%startup_dele[k])
            print startup_dele[k]+' REMOVED FORM THE STARTUP LIST'

startup_delete()
