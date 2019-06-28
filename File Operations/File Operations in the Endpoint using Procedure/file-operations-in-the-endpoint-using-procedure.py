option= '1'  # Please provide option 
#option 1: For renaming a file or folder ## Please edit both file_folderpath and dest_path
#option 2: List files from specified folder ##Please edit only  file_folderpath
#option 3: For hiding a file or folder ##Please edit only  file_folderpath
#option 4: For unhiding a file or folder ##Please edit only  file_folderpath
#option 5: For copying a file or folder  ## Please edit both file_folderpath and dest_path
        ##[Note: For copying a folder contents please give a new folder name in dest_path that will create new folder and copy its contents] 
#option 6: For moving a file file or folder ## Please edit both file_folderpath and dest_path
#option 7: To remove a file or folder ## Please edit only  file_folderpath
#option 8: Get directory size/contents  ##Please edit only  file_folderpath
#option 9: Displaying file creation time ## Please edit only  file_folderpath
#option 10:Getting last file modification time ##Please edit only  file_folderpath

import ctypes
import subprocess        
import urllib
import os
import time
import shutil
import os.path

file_folderpath=r'C:\Users\devil\desktop\sam' #change the path according to the option
dest_path=r'C:\Users\devil\documents\cy' #change the dest_path according to the option

class disable_file_system_redirection: 
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def changename(file_folderpath,dest_path):
    with disable_file_system_redirection():
        if os.path.isdir(file_folderpath):
            print 'it is a folder'
        elif os.path.isfile(file_folderpath):
            print 'it is a file'
        else:
            print 'Sorry! Given path is not available.'
    
def listfiles(file_folderpath):
    with disable_file_system_redirection():
        result=os.listdir(file_folderpath)
        print result
        
def hide(file_folderpath):
    with disable_file_system_redirection():
        if os.path.isdir(file_folderpath):
            print 'it is a folder'
        elif os.path.isfile(file_folderpath):
            print 'it is a file'
        else:
            print 'Sorry! Given path is not available.'
        from subprocess import Popen, PIPE
        if os.path.exists(file_folderpath):
            OBJ = Popen('attrib +H '+file_folderpath, stdin = PIPE, stdout = PIPE, stderr = PIPE, shell=True)
            RES = OBJ.communicate()
            RET = OBJ.returncode
            if RET == 0:
                print file_folderpath+' is hidden successfully'
            else:
                print RES[1]
        else:
            print '1: Sorry! Given path is not available.'
            
def unhide(file_folderpath):
    with disable_file_system_redirection():
        if os.path.isdir(file_folderpath):
            print 'it is a folder'
        elif os.path.isfile(file_folderpath):
            print 'it is a file'
        else:
            print 'Sorry! Given path is not available.'
        from subprocess import Popen, PIPE
        if os.path.exists(file_folderpath):
            OBJ = Popen('attrib -H '+file_folderpath, stdin = PIPE, stdout = PIPE, stderr = PIPE, shell=True)
            RES = OBJ.communicate()
            RET = OBJ.returncode
            if RET == 0:
                print file_folderpath+' is unhidden successfully'
            else:
                print RES[1]
        else:
            print '1: Sorry! Given path is not available.'
            
def copyfile_folder(file_folderpath,dest_path):
    with disable_file_system_redirection():
        from shutil import copytree
        if os.path.isdir(file_folderpath):
            try:
                shutil.copytree(file_folderpath,dest_path)
                print'it is a folder'
                print("%s is copied to %s"%(file_folderpath,dest_path))
            except Exception as err:
                print err
        elif os.path.isfile(file_folderpath):
            try:
                shutil.copy2(file_folderpath,dest_path)
                print'it is a file'
                print("%s is copied to %s"%(file_folderpath,dest_path))
            except Exception as err:
                print err
        else:
            print '1: Sorry! Given path is not available.'

def movefile_folder(file_folderpath,dest_path):
    with disable_file_system_redirection():
        if os.path.isdir(file_folderpath):
            try:
                shutil.move(file_folderpath,dest_path)
                print'it is a folder'
                print("%s is moved to %s"%(file_folderpath,dest_path))
            except Exception as err:
                print err
        elif os.path.isfile(file_folderpath):
            try:
                shutil.move(file_folderpath,dest_path)
                print'it is a file'
                print("%s is moved to %s"%(file_folderpath,dest_path))
            except Exception as err:
                print err
        else:
             print '1: Sorry! Given path is not available.'
                
def removefile_folder(file_folderpath):
    with disable_file_system_redirection():
        if os.path.isdir(file_folderpath):
            try:
                shutil.rmtree(file_folderpath)
                print'it is a folder'
                print("%s is removed successfully"%(file_folderpath))
            except Exception as err:
                print err
        elif os.path.isfile(file_folderpath):
            try:
                os.remove(file_folderpath)
                print'it is a file'
                print("%s is removed succesfully"%(file_folderpath))
            except Exception as err:
                print err
        else:
            print '1: Sorry! Given path is not available.'

def directorysize_contents(file_folderpath):
    with disable_file_system_redirection():
        file_folderpath_size=0
        if os.path.isdir(file_folderpath):
            print"The files in directory"
            i=os.listdir(file_folderpath)
            print i
            for(path, dirs, files) in os.walk(file_folderpath):
                for file in files:
                    filename = os.path.join(path, file)
                    file_folderpath_size += os.path.getsize(filename)
                    print "Size of the Directory %s %s %s MB" %(file_folderpath, '.'*20, round(file_folderpath_size/(1024*1024.0), 2))
        else:
            print('Please provide the valid directory path')
            
def creationtime(file_folderpath):
    with disable_file_system_redirection():
        print time.ctime(os.stat(file_folderpath).st_ctime)

def modifiedtime(file_folderpath):
    with disable_file_system_redirection():
        print time.ctime(os.stat(file_folderpath).st_mtime)

                                                
if option == '1':
    changename(file_folderpath,dest_path)
    os.rename(file_folderpath,dest_path)
    print"Renamed successfully"
elif option=='2':
    print"The files are:"
    listfiles(file_folderpath)
elif option=='3':
    hide(file_folderpath)
elif option=='4':
    unhide(file_folderpath)
elif option=='5':
    copyfile_folder(file_folderpath,dest_path)
elif option=='6':
    movefile_folder(file_folderpath,dest_path)
elif option=='7':
    removefile_folder(file_folderpath)
elif option=='8':
    directorysize_contents(file_folderpath)
elif option=='9':
    print"Creation time"
    creationtime(file_folderpath)
elif option=='10':
    print" The last modified time is"
    modifiedtime(file_folderpath)
else:
    print 'Selected option does not exist'

