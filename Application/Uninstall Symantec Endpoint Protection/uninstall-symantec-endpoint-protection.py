import os,ctypes,re,_winreg,time,platform
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


def checkapp():
    import _winreg
    import os
    AppName=r'Symantec Endpoint Protection'
    AppName = AppName.lower()
    def DNDS(rtkey, pK, kA):
        ln = []
        lv = []
        try:
            oK = _winreg.OpenKey(rtkey, pK, 0, kA)
            i = 0
            while True:
                try:
                    bkey = _winreg.EnumKey(oK, i)
                    vkey = os.path.join(pK, bkey)
                    oK1 = _winreg.OpenKey(rtkey, vkey, 0, kA)
                    try:
                        tls = []
                        DN, bla = _winreg.QueryValueEx(oK1, 'DisplayName')
                        DV, bla = _winreg.QueryValueEx(oK1, 'DisplayVersion')
                        _winreg.CloseKey(oK1)
                        ln.append(DN)
                        lv.append(DV)
                    except:
                        pass
                    i += 1
                except:
                    break
            _winreg.CloseKey(oK)
            return zip(ln, lv)
        except:
            return zip(ln, lv)

    rK = _winreg.HKEY_LOCAL_MACHINE
    sK = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    openedKey = _winreg.OpenKey(rK, sK, 0, _winreg.KEY_READ)
    arch, bla = _winreg.QueryValueEx(openedKey, 'PROCESSOR_ARCHITECTURE')
    arch = str(arch)
    _winreg.CloseKey(openedKey)

    if arch == 'AMD64':
        fList = DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
        fList.extend(DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
        fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ))
        fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
    else:
        fList = DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_READ)
        fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_READ))
    fList = set(fList)

    lr = []
    rs = 0
    for i in fList:
        a, b = i
        if AppName in a.lower():
            lr.append('success: {} is installed'.format(a))
            lr.append('{:<25}{:5}'.format(a, b))
            rs += 1
        else:
            rs += 0
    if rs:
        return True
    return False

def reg():

    blacklist=r'Symantec Endpoint Protection'

    def collectprograms(rtkey,pK,kA):
        try:
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
                        inlist=[DN.strip(), vkey, pK]
                        list.append(inlist)
                        
                    except:
                        pass
                    i+=1
                except:
                    break
        except:
            pass
        return list

        
    uninstallkey_32='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'

    if 'PROGRAMFILES(X86)' in os.environ.keys():
        
        rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey_32,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
                (_winreg.HKEY_LOCAL_MACHINE,uninstallkey_32,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey_32,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey_32,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ)]
    else:
        
        rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey_32,_winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey_32,_winreg.KEY_READ)]

    bet=[]
    for i in rklist:
        col=collectprograms(i[0], i[1], i[2])
        for c in col:
            if blacklist in c:
                bet.append(c[1])

    if not bet:
        print "Please blacklist Valid Installed Software"
    else:
        for i in bet:
            j=i.replace(" ", '" "')
            v='\\'
            path="HKEY_LOCAL_MACHINE"+v+i
            path1="HKEY_LOCAL_MACHINE"+v+j
            got=path1
            
            
    return got



def event():
    k=os.popen('''wevtutil qe Application /rd:true /c:1 /f:text  /q:"*[System[(EventID=11724) and Provider[@Name='MsiInstaller']]]" |findstr /i "Symantec"''').read().strip().split('\n')
    k=filter(None, k)
    if len(k)!=0:
        print "\t\t*)",' '.join(k)


def event2():
    k1=os.popen('''wevtutil qe Application /rd:true /c:1 /f:text  /q:"*[System[(EventID=11725) and Provider[@Name='MsiInstaller']]]" |findstr /i "Symantec"''').read().strip().split('\n')
    k1=filter(None, k1)
    if len(k1)!=0:
        print "\t\t*)",' '.join(k1)

        
def Uninstall_SEP():
    with disable_file_system_redirection():
        fin=reg()
        fina=fin.split('\\')[-1]
        guid=re.findall('{.*}',fina)[0]
        if guid:
            us='MsiExec.exe /I '+guid+' /quiet REBOOT=ReallySuppress REMOVE=ALL'
            out=os.popen(us).read()
            time.sleep(5)
            inst1=checkapp()
            if inst1:
                event2()
            else:
                event()
        else:
            print "GUID reporting Error"
print "Symantec Endpoint protection Uninsalltion Script: \n"
inst1=checkapp()
if inst1:
    print "\t*)Symantec Endpoint protection is installed at the Endpoint\n"
    print "\t*)Uninstallation of Symantec Endpoint protection Started:\n"
    Uninstall_SEP()
else:
    print "\t*)Symantec Endpoint protection is not installed at the Endpoint\n"
