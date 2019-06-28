import os
import time
des_fname=os.environ['COMPUTERNAME']
src_path=r'C:\backlogs'
time_tag=time.strftime('%Y_%m_%d_%H_%M_%S')
dest_path=r'C:\backuplogs' #Provide the path where you need to backup
path= dest_path+'\\'+des_fname +'\\'+time_tag


import ctypes
import os
import shutil
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
    if not os.path.exists(src_path):
        os.makedirs(src_path)
        security=os.popen("wmic nteventlog where filename='security' backupeventlog "+src_path+r"\security.evt").read()
        print security
        system=os.popen("wmic nteventlog where filename='system' backupeventlog "+src_path+r"\system.evt").read()
        print system
        appln=os.popen("wmic nteventlog where filename='application' backupeventlog "+src_path+r"\application.evt").read()
        print appln        
        setup=os.popen("wmic nteventlog where filename='setup' backupeventlog "+src_path+r"\setup.evt").read()
        print setup
        fwdevent=os.popen("wmic nteventlog where filename='forwardedevents' backupeventlog "+src_path+r"\forwardedevents.evt").read()        
        print fwdevent
       
if os.environ['SYSTEMDRIVE']:
    shutil.copytree(src_path,path)
    print '%s please check here for the backup windows event logs'%path
    shutil.rmtree(src_path)
