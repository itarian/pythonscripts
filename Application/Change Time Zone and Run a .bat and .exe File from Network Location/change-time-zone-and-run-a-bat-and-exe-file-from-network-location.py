name='"Syria Standard Time"'   #provide the name of the time zone to be changed
#If name is in string, enclose it in '" "'- eg:'"Syria Standard Time"'
#If name is in String+number, enclose it in " " - eg: "UTC+13"

Filepath=r'\\Audi\c\Users\audiR7\Desktop'            ##Provide the network share file path
share_user="XXXXX"                                             ## Provide the user name for the shared path
share_pass="YYYYY"                                            ## Provide the password for the shared path
Setup_Path_X64=r"qbittorrent_4.1.0_x64_setup.exe"         ## Enter the .exe file name for 64 bit
Setup_Path_X86=r"qbittorrent_4.0.4_setup.exe"                 ## Enter the .exe file name for 32 bit
Bat_file=r"Sample.bat"                  ## Enter the .bat file name
silent_commnad ="/S"                   ## Enter the silent command to install the .exe file

import os
import shutil
import platform
import ctypes
import re
import subprocess

print"-------- TIME ZONE--------\n"

print("The current time zone is")
cur_zon=os.popen("TZUTIL /g ").read()
print cur_zon
print("------CHANGING TIME ZONE------------\n")

change=os.popen("TZUTIL /s "+name).read()
print change

print("The Changed current time zone is")
cur_zone=os.popen("TZUTIL /g ").read()
print cur_zone


path=r"C:\Program Files (x86)"
if os.path.exists(path):
    print "64"
    NFN=Setup_Path_X64    
else:
    NFN=Setup_Path_X86
    print "32"
    
CP=os.path.join(Filepath,NFN)
SP=os.path.join(Filepath,Bat_file)
workdir=os.environ["TEMP"]

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
            
def login(cmd,Filepath,CP):
    with disable_file_system_redirection():        
        print 'Login to network share'
        print os.popen(cmd).read()
        print 'Copying  file from Network share....'
        print os.popen('copy "'+CP+'" '+workdir).read()
        print os.popen('copy "'+SP+'" '+workdir).read()
        
cmd= 'NET USE "'+Filepath+'" /USER:'+share_user+'  "'+share_pass+'"'
login(cmd,Filepath,CP)
PTI=os.path.join(workdir,NFN)
print "Executing .exe file"
os.chdir(workdir)
CMD = '"'+NFN+'"'+" "+silent_commnad
print CMD
a=os.popen(CMD).read()

ATI=os.path.join(workdir,Bat_file)
print "Excuting .bat File"
process = subprocess.Popen([ATI],stdout=subprocess.PIPE)
stdout = process.communicate()[0]
print "---------------------------"
print stdout
