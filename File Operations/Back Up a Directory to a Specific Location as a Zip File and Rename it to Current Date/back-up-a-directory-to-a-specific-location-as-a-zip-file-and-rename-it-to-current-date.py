import os

sc =r'xxxxxxxxxx'          #Provide the source folder path here    
ds =r'xxxxxxxxxx'        #Provide the destination path were the folder need to be copied.

dest1=ds+"\\"+"new123"
src_path=dest1+'new.zip'

zip_file_path=src_path


import shutil
import ctypes
import zipfile
import datetime

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


def zip_item(path, zip_file_path):  # Creating ZIP file
    print "Zipping up the file\n"
    zip_object=zipfile.ZipFile(zip_file_path, 'w')
    from subprocess import Popen, PIPE, call
    if os.path.isfile(path):
        try:
           os.chmod(path,0644)
        except:
            pass
        zip_object.write(path, path.split(os.sep)[-1])
        zip_object.close()
        return zip_file_path
    else:
        length_directory_path=len(path)
        for root, directories, files in os.walk(path):
            for file_name in files:
                try:
                    os.chmod(file_name,0644)
                except:
                    pass
                file_path=os.path.join(root, file_name) 
                zip_object.write(file_path, file_path[length_directory_path:])
        zip_object.close()
        print "Created Zip_file\n"
        return zip_file_path

with disable_file_system_redirection():
    shutil.copytree(sc,dest1)
    zip_item(dest1,zip_file_path)
    a=os.popen("ren "+zip_file_path+" %date:~-10,2%-%date:~7,2%-%date:~-4,4%.zip").read()
    print "File renamed successfully to the current date"
if os.path.exists(dest1):
	shutil.rmtree(dest1)
	
