location =itsm.getParameter('parameterName')
import os
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
import urllib
def main(Path, URL='https://valkyrie.comodo.com/apt_tool/download/UnknownFileHunter.exe'):
    if os.path.exists(Path):
        fn = URL.split('/')[-1]
        fp = os.path.join(Path, fn)
        try:
            with open(fp, 'wb') as f:
                try:
                    f.write(urllib.urlopen(URL).read())
                    print fp
                except Exception as e:
                    print e
        except Exception as e:
            print e
        
    else:
        print 'No path: '+Path+' is exist'

main(location)

