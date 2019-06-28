import os
import ctypes
ps_content=r'''

function pass{
Set-Culture en-GB 
Set-WinSystemLocale en-GB 
Set-WinHomeLocation -GeoId 242 
Set-WinUserLanguageList en-GB -force
}

pass

'''



def ecmd(command):
    import ctypes
    from subprocess import PIPE, Popen
    
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
        obj = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    ret=obj.returncode
    if ret==0:
        if out:
            return out.strip()
        else:
            return ret
    else:
        if err:
            return err.strip()
        else:
            return ret

file_name='powershell_file.ps1'
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
print ecmd('powershell "%s"'%file_path)

print ecmd('REG Add "HKEY_USERS\.DEFAULT\Control Panel\International" /v "Locale" /t "REG_SZ" /d "00000809" /f')
print ecmd('REG Add "HKEY_USERS\.DEFAULT\Control Panel\International" /v "LocaleName" /t "REG_SZ" /d "en-GB" /f')
print ecmd('REG Add "HKEY_USERS\.DEFAULT\Control Panel\International" /v "sCountry" /t "REG_SZ" /d "United Kingdom" /f')
print ecmd('REG Add "HKEY_USERS\.DEFAULT\Control Panel\International" /v "sCurrency" /t "REG_SZ" /d "?" /f')
print ecmd('REG Add "HKEY_USERS\.DEFAULT\Control Panel\International" /v "sLanguage" /t "REG_SZ" /d "ENG" /f')
print ecmd('REG Add "HKEY_USERS\.DEFAULT\Keyboard Layout\Preload" /v "1" /t "REG_SZ" /d "00000809" /f')

try:
    print ecmd('REG Add "HKEY_USERS\S-1-5-18\Control Panel\International" /v "Locale" /t "REG_SZ" /d "00000809" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-18\Control Panel\International" /v "LocaleName" /t "REG_SZ" /d "en-GB" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-18\Control Panel\International" /v "sCountry" /t "REG_SZ" /d "United Kingdom" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-18\Control Panel\International" /v "sCurrency" /t "REG_SZ" /d "?" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-18\Control Panel\International" /v "sLanguage" /t "REG_SZ" /d "ENG" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-19\Control Panel\International" /v "Locale" /t "REG_SZ" /d "00000809" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-19\Control Panel\International" /v "LocaleName" /t "REG_SZ" /d "en-GB" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-19\Control Panel\International" /v "sCountry" /t "REG_SZ" /d "United Kingdom" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-19\Control Panel\International" /v "sCurrency" /t "REG_SZ" /d "?" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-19\Control Panel\International" /v "sLanguage" /t "REG_SZ" /d "ENG" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-20\Control Panel\International" /v "Locale" /t "REG_SZ" /d "00000809" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-20\Control Panel\International" /v "LocaleName" /t "REG_SZ" /d "en-GB" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-20\Control Panel\International" /v "sCountry" /t "REG_SZ" /d "United Kingdom" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-20\Control Panel\International" /v "sCurrency" /t "REG_SZ" /d "?" /f')
    print ecmd('REG Add "HKEY_USERS\S-1-5-20\Control Panel\International" /v "sLanguage" /t "REG_SZ" /d "ENG" /f')
except:
    pass
os.remove(file_path)

