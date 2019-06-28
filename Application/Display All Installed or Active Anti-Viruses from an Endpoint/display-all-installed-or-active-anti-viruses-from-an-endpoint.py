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
    if not RET:
        if OUT == True:
            if out:
                return out.strip()
            else:
                return True
        else:
            return True
    else:
        return False

text=ExecuteCMD(r'WMIC /Node:localhost /Namespace:\\root\SecurityCenter2 Path AntiVirusProduct Get displayName /Format:List', True)
third=''
windows=''
for i in text.split('\n'):
    if i.strip():
        for j in i.split('='):
            if not j=='displayName':
                if 'windows' in j.lower():
                    windows+=j+'\n'
                else:
                    third+=j+'\n'
if third:
    print 'Third Party Anti Viruses:'
    print third
else:
    print 'No third party Anti Virus found :('

if windows:
    print 'Windows Anti Virus Tool:'
    print windows
else:
    print 'No Windows Defender found :('
