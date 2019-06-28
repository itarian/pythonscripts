ApplicationName='Sentinel Agent'
URL=r'https://carvir-msp02.sentinelone.net/web/api/v2.0/update/agent/download/335191984708020342/325059810296864373'
SilentCommand='/S'
DownloadPath='%temp%'
FileName='Sentinel Agent'
Extension='.exe'
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

## Execute CMD
def ExecuteCMD(CMD, OUT = False):
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
    RET = OBJ.returncode
    if RET == 0:
        if OUT == True:
            if out != '':
                return out.strip()
            else:
                return True
        else:
            return True
    return False

## If pattern is given, converts to real path
def PaternPath(DownloadPath):
    import os
    if not os.path.isdir(DownloadPath):
        return ExecuteCMD('echo '+DownloadPath, True)
    return DownloadPath

## Downloads application
def Download(Path, URL, FileName, Extension):
    import urllib2
    import os
    fn = FileName+Extension
    fp = os.path.join(Path, fn)
    req = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req)
    with open(fp, 'wb') as f:
        while True:
            chunk=con.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    if os.path.exists(fp):
        return fp
    return False

## Install Application with Silent Command
def Install(FilePath, SilentCommand):
    if not (FilePath[-4:-1]+FilePath[-1]).lower()=='.msi':
        return ExecuteCMD('"'+FilePath+'" '+SilentCommand)
    else:
        return ExecuteCMD('msiexec /i "'+FilePath+'" '+SilentCommand)

## Check whether the app is installed
def CheckApp(AppName):
    import _winreg
    import os
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

import os
if not CheckApp(ApplicationName):
    Path=PaternPath(DownloadPath)
##    print Path
    FilePath=Download(Path, URL, FileName, Extension)
##    print FilePath
    if Install(FilePath, SilentCommand):
        print FilePath+' is installed now successfully :)'
    os.remove(FilePath)
else:
    print ApplicationName+' is already installed'

