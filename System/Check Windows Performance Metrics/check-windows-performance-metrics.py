import xml.etree.ElementTree as ET
import os

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

## Execute CMD 'WinSAT Prepop'
CMDRES = ExecuteCMD('WinSAT Prepop')

## Collect XML Tree Objects for all Prepop XML files
XMLDIRPATH = os.path.join(os.environ['WINDIR'], r'Performance\WinSAT\DataStore')
if os.path.isdir(XMLDIRPATH):        
    FILES = os.listdir(XMLDIRPATH)
    FILES.reverse()
    for FILE in FILES:
        if FILE.endswith('.xml'):
    ##        if FILE.endswith('.xml') and '(Prepop)' in FILE:
            XMLFILEPATH = os.path.join(XMLDIRPATH, FILE)
            print XMLFILEPATH
            print '-'*50
            tree = ET.parse(XMLFILEPATH)
            RT = tree.getroot()
            for i in RT.getchildren():
                if i.text:
                    print i.tag, i.text
                    for j in i.getchildren():
                        if j.text:
                            print '{0:30}{1:30}'.format(j.tag, j.text)
                else:
                    print i.tag
                    print '-'*50
                    for j in i.getchildren():
                        if j.text:
                            print '{0:30}{1:30}'.format(j.tag, j.text)
                print '-'*50
                print '\n'
else:
    print '{} is not available'.format(XMLDIRPATH)
