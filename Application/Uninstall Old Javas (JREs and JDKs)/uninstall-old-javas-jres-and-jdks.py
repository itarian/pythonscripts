def DNDS(rtkey,pK,kA):
    import re
    ln=[]
    lv=[]
    lus=[]
    try:
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
                    US,bla=_winreg.QueryValueEx(oK1,'UninstallString')
                    _winreg.CloseKey(oK1)
                    o=re.search(r'(^java.*|^j2se.*)update.*',DN.lower())
                    if o.group():
                        ln.append(DN)
                        lv.append(DV)
                        lus.append(US)
                except:
                    pass
                i += 1
            except:
                break
        _winreg.CloseKey(oK)
        return zip(ln,lv,lus)
    except:
        return zip(ln,lv,lus)

def ecmd(CMD):
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
    r=OBJ.returncode
    return r

import _winreg
import os
if 'PROGRAMFILES(X86)' in os.environ.keys():
    f=DNDS(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
    f.extend(DNDS(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
    f.extend(DNDS(_winreg.HKEY_CURRENT_USER,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ))
    f.extend(DNDS(_winreg.HKEY_CURRENT_USER,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
else:
    f=DNDS(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',_winreg.KEY_READ)
    f.extend(DNDS(_winreg.HKEY_CURRENT_USER,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',_winreg.KEY_READ))

if len(f)>0:
    vf=[]
    df=[]
    for i in f:
        vf.append([str(i[0]), [int(k) for k in i[1].split('.')], str(i[2])])
    vf=sorted(vf,key=lambda x:x[1],reverse=True)

    print 'Existing JREs: '
    for i in vf[:]:
        if 'Development' not in i[0]:
            print i[0], '.'.join([str(k) for k in i[1]])
        else:
            vf.remove(i)
            df.append(i)
            
    if len(df)>0:
        print '\n'
        print 'Existing JDKs: '
        for i in df:
            print i[0], '.'.join([str(k) for k in i[1]])

    if len(df)>1:
        print '\n'
        print 'Removed JDKs: '
        if len(df[2:])>0:
            for i in df[2:]:
                if ecmd(i[-1].replace('MsiExec.exe /I', 'MsiExec.exe /X')+' /qn')==0:
                    print i[0], '.'.join([str(k) for k in i[1]])
        if df[0][1]==df[1][1]:
            for i in df[:2]:
                if '(64-bit)' not in i[0]:
                    if ecmd(i[-1].replace('MsiExec.exe /I', 'MsiExec.exe /X')+' /qn')==0:
                        print i[0], '.'.join([str(k) for k in i[1]])
        else:
            if ecmd(df[1][-1].replace('MsiExec.exe /I', 'MsiExec.exe /X')+' /qn')==0:
                print df[1][0], '.'.join([str(k) for k in df[1][1]])

    if len(vf)>1:
        print '\n'
        print 'Removed JREs: '
        if len(vf[2:])>0:
            for i in vf[2:]:
                if ecmd(i[-1].replace('MsiExec.exe /I', 'MsiExec.exe /X')+' /qn')==0:
                    print i[0], '.'.join([str(k) for k in i[1]])
        if vf[0][1]==vf[1][1]:
            for i in vf[:2]:
                if '(64-bit)' not in i[0]:
                    if ecmd(i[-1].replace('MsiExec.exe /I', 'MsiExec.exe /X')+' /qn')==0:
                        print i[0], '.'.join([str(k) for k in i[1]])
        else:
            if ecmd(vf[1][-1].replace('MsiExec.exe /I', 'MsiExec.exe /X')+' /qn')==0:
                print vf[1][0], '.'.join([str(k) for k in vf[1][1]])
else:
    print 'No Java Installed'
