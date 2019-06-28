#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name
quick_icon_name=itsm.getParameter('Icon_Name')  #Replace your preferred Icon's name

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
            
os_drive=os.environ['SYSTEMDRIVE']
path=os.path.join(os_drive,r'\Users')
Icon_found=0

try:
    for users in os.listdir(path):
        t=os.path.join(path,users)
        full_path=os.path.join(t, 'AppData','Roaming','Microsoft','Internet Explorer','Quick Launch','User Pinned','TaskBar')
        if os.path.exists(full_path):           
            try:
                for icons in os.listdir(full_path):
                    if quick_icon_name.lower()==icons.lower():
                        j=os.path.join(full_path,icons)
                        os.remove(j)
                        print 'Successfully Removed the "%s" Icon........' %quick_icon_name
                        Icon_found+=1
                        break
            except Exception as err:
                print 'Failed due to the below error'
                print err
except Exception as err:
    print 'Failed due to the below error'
    print err

if not Icon_found:
    print 'The Quick Icon "%s" does not Exist\n'%quick_icon_name
