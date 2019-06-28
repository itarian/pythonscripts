kayako_ticket_number="Testing"

import urllib2
import os
import shutil
import zipfile
import time
import ctypes
import re
import sys
from subprocess import PIPE, Popen

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
        try:
            shutil.copytree(source_path, destination_folder)
        except:
            shutil.copy(source_path, destination_folder)
            pass
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
temp_folder='temp_logs'
work_directory=os.path.join(os.getenv('programdata'), temp_folder)
if os.path.exists(work_directory):
	try:
		shutil.rmtree(work_directory)
	except:
		print "You are intiating the script for the second time, Please try again after 15 Minutes"
		import sys
		sys.exit(0)
## Collects CCC Logs
time_tag=time.strftime('%Y_%m_%d_%H_%M_%S')
c1_file_name='%s_PMLogData_%s_%s.zip'%(kayako_ticket_number, computer_name, time_tag)
c1_log_zip_file=os.path.join(os.getenv('programdata'), c1_file_name)
win_update_path=r'C:\Windows\WindowsUpdate.log'

def windows_update():
    ps_content=r'''
    Get-WindowsUpdateLog -LogPath "C:\Windowsupdate.log"
    '''
    import os

    file_name='powershell_file.ps1'
    file_path=os.path.join(os.environ['TEMP'], file_name)
    with open(file_path, 'wb') as wr:
        wr.write(ps_content)

    ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
    print ecmd('powershell "%s"'%file_path)
    
    os.remove(file_path)
    windows_folder="C:\Windowsupdate.log"
    return windows_folder 


if os.path.isfile(win_update_path):
    print "Windows Update log is present"
    windows_folder=r'C:\Windows\WindowsUpdate.log'
    with open (windows_folder,"r") as f:
        ki=f.read()
    if "Get-WindowsUpdateLog" in ki:
        windows_folder=windows_update()
    else:
        windows_folder=r'C:\Windows\WindowsUpdate.log'
    print windows_folder
    

if 'PROGRAMW6432' in os.environ.keys():
    main_directory=r"C:\Program Files (x86)\COMODO\Comodo ITSM"
    log_files=[r"C:\Program Files (x86)\COMODO\Comodo ITSM\pm.db",
               r"C:\Program Files (x86)\COMODO\Comodo ITSM\pmlogs\Pm_Service.log",
               r"C:\Program Files (x86)\COMODO\Comodo ITSM\pmlogs\PmAgent.log",
               r'C:\Program Files (x86)\COMODO\Comodo ITSM\pmagent.dll',
               windows_folder]
    log_folders=[r"C:\Program Files (x86)\COMODO\Comodo ITSM\pmlogs"]
else:
    main_directory=r"C:\Program Files\COMODO\Comodo ITSM"
    log_files=[r"C:\Program Files\COMODO\Comodo ITSM\pmlogs\Pm_Service.log",
               r"C:\Program Files\COMODO\Comodo ITSM\pmlogs\PmAgent.log",
               r"C:\Program Files\COMODO\Comodo ITSM\pmagent.dll",
               r'C:\Program Files\COMODO\Comodo ITSM\pm.db',
               windows_folder]
    log_folders=[r"C:\Program Files\COMODO\Comodo ITSM\pmlogs"]
data_logs_folder="C:\\ProgramData\\COMODO\\Comodo ITSM\\logs"

for root, folders, files in os.walk(main_directory):
    for file_name in files:
        if file_name.lower().endswith('.dmp'):
            path=os.path.join(root, file_name)
            log_files.append(path)
print "Collecting PM Logs"
print "***********"
print "copying Pm_Service.log"
print "Copied Pm_Service.log"
print "copying PmAgent.log"
print "Copied PmAgent.log"
print "copying pmagent.dll"
print "Copied pmagent.dll"
print "copying pmlogs"
print "Copied pmlogs"
print "Copying Windows Update.log"
print "Copied Windows Update.log"
print "******"

ccc_log_directory=os.path.join(os.getenv('programdata'), 'ccc_logs')
##if os.path.exists(ccc_log_directory):
##	sys.exit(0)
try:
	os.mkdir(ccc_log_directory)
except:
	pass
log_files.extend(log_folders)
for i in log_files:
    copy(i, ccc_log_directory)
if os.listdir(ccc_log_directory):
    print 'Collecting PMLOGs %s Done'%('.'*15)
else:
    print 'Failed to Collect PMLOGs'

## Transfers File
zip_item(ccc_log_directory, c1_log_zip_file)

winscp_file_path=os.path.join(work_directory, 'WinSCP_C1_SFTP.exe')

winscp_url=r"https://patchportal.one.comodo.com/portal/packages/spm/DYMO Label Software/x86/WinSCP.exe"

os.mkdir(work_directory)
winscp_program_path=download(winscp_url, winscp_file_path)
winscp_script_file=os.path.join(work_directory, 'script_winscp.txt')
if sftp_transfer(winscp_program_path, winscp_script_file, c1_log_zip_file)==0:
	print 'Transfering PMLOGs %s Done'%('.'*15)
else:
	print 'Failed to Transfer PMLOGs'
ki=os.environ['TEMP']
os.chdir(ki)
try:
    shutil.rmtree(work_directory)
except:
    pass
try:
    os.remove(file2)
except:
    pass

try:
    shutil.rmtree(ccc_log_directory)
except:
    pass


