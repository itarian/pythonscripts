kayako_ticket_number="xxxxxxxx"
BAT="""
@echo off

rem example of usage:
rem change_debug_mode_crc.bat [enabled_key] [level_key] [crhost_verbose_level_key]
rem change_debug_mode_crc.bat 1 1 3

set registry_path="HKEY_CURRENT_USER\SOFTWARE\COMODO\CRControl\Debug"
set enabled_key="Enabled"
set level_key="Level"
set crhost_verbose_level_key="CRHostVerboseLevel"


goto:main

:main
if "%1"=="" (
call:show_hint
) else (
call:add_registry_path %registry_path% %enabled_key% %1
call:add_registry_path %registry_path% %level_key% %2
call:add_registry_path %registry_path% %crhost_verbose_level_key% %3)
goto:eof

:add_registry_path
call reg add %~1 /v %~2 /t REG_DWORD /d %~3 /f
goto:eof

:show_hint
echo "Params can't be empty. Input next params: [enabled_key] [level_key] [crhost_verbose_level_key]"
echo "Enabled values: 0 | 1"
echo "Level values: 0 - 4 (QtDebugMsg, QtWarningMsg, QtCriticalMsg, QtFatalMsg, QtInfoMsg)"
echo "CRHostVerboseLevel values: 0 - 9"
goto:eof
"""
import urllib2
import os
import getpass
import shutil
import zipfile
import time
import ctypes
import sys
import subprocess
from subprocess import PIPE,Popen

bat_path=os.environ['PROGRAMDATA'] +"\\" +"Sample.bat"
def bat_run(path):
    with open(bat_path,"w") as f:
        f.write(BAT)
    b=bat_path+" "+"1 0 9"
    process =subprocess.Popen(b,stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    print stdout
if os.path.exists(bat_path):
	try:
		os.remove(bat_path)
	except:
		sys.exit(0)
bat_run(bat_path)
def copy(source_path, destination_path):
    if os.path.isfile(source_path):
        with open(source_path, 'rb') as reader:
            data=reader.read()
        destination_file=os.path.join(destination_path, source_path.split(os.sep)[-1])
        with open(destination_file, 'wb') as writer:
            writer.write(data)
        return destination_file
    else:
        destination_folder=os.path.join(destination_path, source_path.split(os.sep)[-1])
        shutil.copytree(source_path, destination_folder)
        return destination_folder

def download(url, file_path): ### Downloading
    try:
        import urllib2
        import os
        request = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        parsed = urllib2.urlopen(request)
        with open(file_path, 'wb') as f:
            while True:
                chunk=parsed.read(100*1000*1000)
                if chunk:
                    f.write(chunk)
                else:
                    break
        return file_path
    except:
        url_object=urllib2.urlopen(url)
        download_data=url_object.read()
        with open(file_path, "wb") as writer:
            writer.write(download_data)
        return file_path
def zip_item(path, zip_file_path):  # Creating ZIP file 

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
        return zip_file_path
    
def sftp_transfer(winscp_program_path, script_path, file_to_send):
    script_code=r"""
open sftp://c1report:paT7rObeseW0duLl@c1report.comodo.com/ -hostkey=*
cd /reports
put "%s"
close
exit
"""%file_to_send
    with open(script_path, "w") as writer:
        writer.write(script_code)
    os.chdir(os.path.join(os.getenv('programdata'),'temp_logs'))
    transfer_object=Popen('%s /script="%s"'%("WinSCP_C1_SFTP.exe", script_path), shell=True, stdout=PIPE, stderr=PIPE)
    transfer_object.communicate()
    os.chdir(os.path.join(os.getenv('programdata')))
    return transfer_object.returncode    


def ecmd(command, output=False):
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
        objt = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = objt.communicate()
    ret=objt.returncode
    if not output:
        return ret
    else:
        return '%s\n%s'%(out, err)

computer_name=os.getenv('computername')


## Collects CRC Logs

drive=os.environ['SystemDrive']
def collect_logs():
    USER=os.popen("wmic useraccount get Name").read()
    Name=[i.strip() for i in  USER.split("\n") if i.strip()]
    Profile=Name[1:]
    AllPaths=[]
    for j in Profile:
        path1=""
        work_directory=""
        if j=="Administrator":
                continue
        elif j=="Guest":
                continue
        else:
            work_directory=""
            User_directory=""
            work_directory=os.path.join(os.environ['PROGRAMDATA'] ,"temp_folder")
            if not os.path.isdir(work_directory):
                os.mkdir(work_directory)
            temp123 = drive+"\\Users\\%s\\AppData\\Local\\CRControl" %(j)
            temp123.replace("/*.*"," ")
            
            if os.path.exists(temp123):
                print "Collecting CRC Logs"
                print "Collecting logs for "+j + " User"
                
                path1=copy(temp123,work_directory)
                base=os.path.join(os.environ['PROGRAMDATA'] ,"temp_folder")
                old_name="CRControl"
                new_name="CRControl _"+j+"User"
                path1=os.path.join(base, new_name)
                os.rename(os.path.join(base, old_name),path1)
                AllPaths.append(path1)
                
                
                
            else:
                print "Crc Logs are not present for "+j+" user"
    if len(AllPaths)==0:
        return 0
    else:
        return AllPaths
                    
AllPaths=collect_logs()
time_tag=time.strftime('%Y_%m_%d_%H_%M_%S')


winscp_directory=os.path.join(os.environ['PROGRAMDATA'] ,"Winscp_download")

if os.path.exists(winscp_directory):
    try:
        shutil.rmtree(winscp_directory)
        time.sleep(1)
    except:
        print "You are intiating the script for the second time, Please try again after 15 Minutes"
        import sys
        sys.exit(0)
    
os.mkdir(winscp_directory)
winscp_file_path=os.path.join(winscp_directory, 'WinSCP_C1_SFTP.exe')
os.chdir(os.environ['SYSTEMDRIVE'])
winscp_url="https://patchportal.one.comodo.com/portal/packages/spm/DYMO%20Label%20Software/x86/WinSCP.exe"
winscp_program_path=download(winscp_url, winscp_file_path)
winscp_program_path=winscp_file_path

if AllPaths==0:
    print "There is no CRC Installed on Endpoint"

else:
    work_directory=os.path.join(os.environ['PROGRAMDATA'] ,"temp_folder")
    c1_file_name='%s_CRCLogDataSource_%s_%s.zip'%(kayako_ticket_number, computer_name, time_tag)
    c1_log_zip_file=os.path.join(os.environ['PROGRAMDATA'], c1_file_name)
    zippath=zip_item(work_directory,c1_log_zip_file)
    winscp_script_file=os.path.join(winscp_directory, 'script_winscp.txt')
    if sftp_transfer(winscp_program_path, winscp_script_file, c1_log_zip_file)==0:
            print 'Transfering CRCLOGs %s Done'%('.'*15)
    else:
            print 'Failed to Transfer CRCLOGs'
    
    try:
        os.remove(c1_log_zip_file)
    except:
        pass
try:
    shutil.rmtree(work_directory)
except:
    pass
try:
    shutil.rmtree(winscp_directory)
except:
        pass
try:
	os.remove(os.remove(os.environ['PROGRAMDATA'] +"\\" +"Sample.bat"))
except:
	pass
