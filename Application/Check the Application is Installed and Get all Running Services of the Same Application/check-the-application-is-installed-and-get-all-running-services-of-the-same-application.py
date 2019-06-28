AppName = 'sophos' ## Provide the Application Name here
import re
import _winreg
import os
from subprocess import PIPE, Popen
ServiceString = AppName
AppName = AppName.lower()
ServiceString = ServiceString.lower()
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
        lr.append('{:<25}{:5}'.format(a, b))
        rs += 1
    else:
        rs += 0

if rs > 0:
    print 'success: applications installed for {}..'.format(AppName)
    for i in lr:
        print i
    OB = Popen('net start | find /i "'+ServiceString+'"', stderr = PIPE, stdout = PIPE, shell=True)
    OUT, ERR = OB.communicate()
    RC = OB.returncode
    if RC == 0:
        print '\nsuccess: started services for {}..'.format(AppName)
        for spl in OUT.split('\n'):
            print spl.strip()
    else:
        print '\nfail: sorry, no service started for {}.'.format(AppName)
else:
    print 'fail: sorry, {} is not installed'.format(AppName)
