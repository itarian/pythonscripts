blacklist=['Manager', 'Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161', 'Microsoft Visual C++ 2015 x64 Additional Runtime - 14.0.23026', 'PDF Architect 5', 'Pidgin', 'VLC media player', 'Microsoft Visual C++ 2015 Redistributable (x86) - 14.0.24215']
def ecmd(CMD, OUT=False):
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
                        us=ecmd(c[3].replace('MsiExec.exe /I', 'MsiExec.exe /X')+' /qn')
                        if us==0:
                            uninstalled+='%d %s == %s\n'%(uc+1, c[0], c[1])
                            uc+=1
                        else:
                            error+='%d %s == %s - error code %d\n'%(ec+1, c[0], c[1], us)
                            ec+=1
                    else:
                        hasnoss.append('%s\n'%(citer))
                    ic+=1
            collected+=citer+'\n'
if blacklisted:
    print 'blacklisted programs found on your endpoint %s: \n%s'%(os.environ['COMPUTERNAME'], blacklisted)
    if uninstalled:
        print '\nprograms which are removed successfully: \n', uninstalled
    if error:
        print '\nerror at removing the programs: \n', error
    if hasnoss:
        print 'programs required user interaction to remove them (not removed by the procedure):'
        cc=0
        for h in hasnoss:
            print '%d %s == %s'%(cc+1, h.split('|')[0], h.split('|')[1])
            cc+=1
else:
    print 'no programs installed on your endpoint %s from your blacklist, here is your blacklisted programs'%os.environ['COMPUTERNAME']
    if blacklist:
        c=0
        for i in blacklist:
            if i==blacklist[-1]:
                print c+1, i+'\n'
                c+=1
            else:
                print c+1, i
                c+=1
