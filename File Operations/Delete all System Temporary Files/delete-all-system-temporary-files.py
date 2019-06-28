import os
drive=os.environ['SYSTEMROOT']
programdata = os.environ['PROGRAMDATA']
systemdrive = os.environ['SYSTEMDRIVE']



File_Clean01 = [drive+r"\System32\Sysprep\Panther",
                drive+r"\Panther",
                drive+r"\Memory.dmp",
		drive+r"\Downloaded Program Files"]

File_Clean02 = [drive+r"\INF"]
 
File_Clean03 = [drive+r"\Minidump"]
 
File_Clean04 = [drive+r"\Temp"]
 
File_Clean05 = []
 
File_Clean06 = [programdata+r"\Microsoft\Windows\WER\ReportArchive",
                programdata+r"\Microsoft\Windows\WER\ReportQueue"]
 
File_Clean07= [drive+r"\SoftwareDistribution\Download"]



import os
import shutil
import stat
import ctypes
from _winreg import *


User= os.popen("wmic useraccount  get Name").read()

User_List =[i.strip() for i in User.split('\n') if i.strip() if i.strip() != 'Name']
System_Drive = os.environ['systemdrive']
os.chmod(System_Drive,0644)

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

for i in User_List:
    file1 = systemdrive+"\\Users\\"+i+"\\AppData\\Local\\Microsoft\\Windows\\Explorer"
    file2 = systemdrive+"\\Users\\"+i+"\\AppData\\Local\\Microsoft\\Windows\\WER\\ReportArchive"
    file3 = systemdrive+"\\Users\\"+i+"\\AppData\\Local\\Microsoft\\Windows\\WER\\ReportQueue"
    file4 = systemdrive+"\\Users\\"+i+"\\AppData\Local\Temp"
    File_Clean05.append(file1)
    File_Clean01.append(file2)
    File_Clean01.append(file3)
    File_Clean04.append(file4)

def clear_folders(File_Clean01):
    print "Deletion of System Log files,System archived Windows Error Reporting,System queued Windows Error Reporting, Delivery Optimization Files Begins...."
    os.chdir(System_Drive)
    for f in File_Clean01:
        if os.path.exists(f):
            for dirpath, dirnames, files in os.walk(f):
                for i in files:
                    i = os.path.join(dirpath,i)
                    os.chmod(i,0644)
                    try:
                        with disable_file_system_redirection():
                            os.remove(i)
                        print "Deleted "+ i
                    except Exception as error:
                        print error
                        pass

def clear_files(File_Clean02):
    os.chdir(System_Drive)
    for i in File_Clean02:
        for dirpath, dirnames, files in os.walk(i):
            for i in files:
                if i.startswith('setupapi'):
                    if i.endswith('.log'):
                        i = os.path.join(dirpath,i)
                        print i
                        with disable_file_system_redirection():
                            os.chmod(i,0644)
                            os.remove(i)
                        print "Deleted " + i


def clear_dmp(File_Clean03):
    os.chdir(System_Drive)
    for i in File_Clean03:
        for dirpath, dirnames, files in os.walk(i):
            for i in files:
                if i.endswith('.dmp'):
                    with disable_file_system_redirection():
                        i = os.path.join(dirpath,i)
                        os.chmod(i,0644)
                        os.remove(i)
                    print "Deleted " + i
            


def clear_temp(File_Clean04):
    print "Deletion of temporary files Begins...."
    print "                                 "
    print "Deletion of Temporary internet files Begins...."
    for f in File_Clean04:
        for dirpath, dirnames, files in os.walk(f):
            for i in dirnames:
                i = os.path.join(dirpath,i)
                os.chdir(dirpath)
                try:
                    os.chmod(i,0644)
                    shutil.rmtree(i)
                    print "Deleted "+ i
                except Exception as error:
                    print error
                    pass
            for i in File_Clean04:
                for dirpath, dirnames, files in os.walk(i):
                    for i in files:
                        i = os.path.join(dirpath,i)
                        try:
                            with disable_file_system_redirection():
                                os.chmod(i,0644)
                                os.remove(i)
                            print "Deleted " + i
                        except Exception as error:
                            print "The process cannot access the file because it is being used by another process: " +  i 
                            pass

def clear_thumbnail(File_Clean05):
    print "The Deletion of Thumbnail caches Begins...."
    add = os.popen('reg add "HKCU\SOFTWARE\Policies\Microsoft\Windows\Explorer" /v DisableThumbsDBOnNetworkFolders /d 0x1 /t REG_DWORD /f').read()
    for f in File_Clean05:
        for dirpath, dirnames, files in os.walk(f):
            for i in files:
                i = os.path.join(dirpath,i)
                os.chdir(dirpath)
                try:
                    with disable_file_system_redirection():
                        os.remove(i)
                    print "Deleted "+ i
                except Exception as error:
                    print "The process cannot access the file because it is being used by another process: " +  i 
                    pass

print "Disk Clean Process has started..."
print "                                 "
print "Scanning for the files..."
print "                                 "
print "Starting to delete the Files..."
print "                                 "
clear_files(File_Clean02)
clear_dmp(File_Clean03)
print "The fils are deleted "
clear_temp(File_Clean04)
print "The Temp files has been deleted"
print "                                 "
clear_thumbnail(File_Clean05)
print "The Thumbnail caches has been deleted"
print "                                     "
print "Deletion of System Log files Begins..." 
clear_folders(File_Clean01)
print "System Log files has been deleted"
print "                                 "
print "Deletion of System archived Windows Error Reporting,System queued Windows Error Reporting Begins...."
clear_folders(File_Clean06)
print "System archived Windows Error Reporting files has been deleted"
print "                                 "
print "Deletion of Delivery Optimization Files"
clear_folders(File_Clean07)
print "Delivery Optimization Files has been deleted"
print "                                 "
reset = os.popen('reg add "HKCU\SOFTWARE\Policies\Microsoft\Windows\Explorer" /v DisableThumbsDBOnNetworkFolders /d 0 /t REG_DWORD /f').read()

