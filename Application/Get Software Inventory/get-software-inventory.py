def computername():
    import os
    return os.environ['COMPUTERNAME']

## get ip address
def ipaddress():
    import socket
    return socket.gethostbyname(socket.gethostname())
## detect all installed software through registry key            
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

## detect whether the computer is 32 bit or 64 bit
import _winreg
import os
print "Computer Name : " +computername()
print "IP-Address : "+ipaddress()
print "\nThe software which is installed on the endpoint \n"
rK = _winreg.HKEY_LOCAL_MACHINE
sK = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
openedKey = _winreg.OpenKey(rK, sK, 0, _winreg.KEY_READ)
arch, bla = _winreg.QueryValueEx(openedKey, 'PROCESSOR_ARCHITECTURE')
arch = str(arch)
_winreg.CloseKey(openedKey)
## sorting all collected data from all the way, filtered duplicates and listed the final result!
if arch == 'AMD64':
    fList = DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
    fList.extend(DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
    fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ))
    fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
else:
    fList = DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_READ)
    fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_READ))
fList = set(fList)
j = 1
for i in sorted(fList):
    a, b = i
    try:
        print '{:<3} {:<100} {:>20}'.format(j, a.encode('utf-8'), b.encode('utf-8'))
    except:
        print j, a, b
    j += 1
