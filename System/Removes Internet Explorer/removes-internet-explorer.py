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

with disable_file_system_redirection():
    try:
        drive=os.getenv("SystemDrive")
        bit_check=os.path.join(drive,r'\Program Files (x86)')
        if os.path.exists(bit_check):
            disable_IE=r'Internet-Explorer-Optional-amd64'
        else:
            disable_IE=r'Internet-Explorer-Optional-x86'
    except Exception as err: 
        print "Failed due to the below error"
        print err

    try:
        cmd=os.popen('DISM /online /get-featureinfo /featurename:%s'%(disable_IE)).read()
        if "Enabled" in cmd:
            cmd1=os.popen('DISM /online /Disable-Feature /FeatureName:%s'%(disable_IE)).read()
            if "successfully." in cmd1:
                print 'Successfully!!! disabled the Internet Explorer..........'
                print 'Please restart your endpoint to apply changes.......'
            else:
                print 'ERROR - Disabling the Internet Explorer Failed......'
        elif "Disable Pending" in cmd:
            print 'Internet Explorer was disabled,please restart to apply changes.......'
        elif "Disabled" in cmd:
            print 'Internet Explorer was disabled already........'
        else:
            print 'ERROR - Disabling the Internet Explorer Failed......'       
    except Exception as err: 
        print "Failed due to the below error"
        print err
