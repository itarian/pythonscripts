import os
PATH = ''
for i in range(10, 17):
    PATH32ON64 = "C:\Program Files (x86)\Microsoft Office\Office{}\OSPP.VBS".format(i)
    PATH32ON32OR64ON64 = "C:\Program Files\Microsoft Office\Office{}\OSPP.VBS".format(i)
    if os.path.isfile(PATH32ON64):
        PATH = PATH32ON64
        break
    elif os.path.isfile(PATH32ON32OR64ON64):
        PATH = PATH32ON32OR64ON64
        break
    else:
        PATH = False

## Function to Execute CMD through Subprocess Module
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
    else:
        return False

if PATH:
    print ExecuteCMD('CScript "'+PATH+'" /dstatus', True)
else:
    print 'MS Office is not found!'