src_path=r'C:\backuplogs'
share_path=r'\\DESKTOP-9QC9TEL\cat'###provide your network share path
des_fname='FILE'##file name in share
share_user="cat" ###username of network share
share_pass="comodo"### password of network share


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
        security=os.popen("wmic nteventlog where filename='security' backupeventlog "+src_path+r"\security.evt").read();
        print security
        system=os.popen("wmic nteventlog where filename='system' backupeventlog  "+src_path+r"\system.evt").read();
        print system
        appln=os.popen("wmic nteventlog where filename='application' backupeventlog "+src_path+r"\application.evt").read();
        print appln
        
        setup=os.popen("wmic nteventlog where filename='setup' backupeventlog "+src_path+r"\setup.evt").read();
        print setup
        fwdevent=os.popen("wmic nteventlog where filename='forwardedevents' backupeventlog "+src_path+r"\forwardedevents.evt").read();
        print fwdevent


    cmd='NET USE "'+share_path+'" /USER:'+share_user+'  "'+share_pass+'"'
    tar_path=share_path+'\\'+des_fname
    print 'Login to network share'
    with disable_file_system_redirection():
        print os.popen(cmd).read()
    print 'Copying files to local machine....'
    try:
        if os.path.isdir(src_path):
            shutil.copytree(src_path,tar_path)
            print 'successfully transfered'
            if os.environ['SYSTEMDRIVE']:
                shutil.rmtree(src_path)
        else:
           print '%s is not found'%src_path
    except Exception as err:
        print err
