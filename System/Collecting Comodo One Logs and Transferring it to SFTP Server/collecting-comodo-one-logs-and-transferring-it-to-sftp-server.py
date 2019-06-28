kayako_ticket_number="GOI-221-286602"
import os
import urllib2
import shutil
from shutil import copyfile
import zipfile
import time
from subprocess import PIPE, Popen

import ctypes
def copy(sourcefile,destinationfile):
    shutil.copy2(sourcefile,destinationfile)

    
class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
def cmd(CMD, OUT = False):
    import ctypes
    
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    RET = OBJ.returncode
    if RET == 0:
        if OUT == True:
            if out != '':
                return out.strip()
            else:
                return True
        else:
            return True
    return False

def CISdata(srcpath,log_folder):
    print "Copying CCS Data "
    os.mkdir(log_folder+'\CCSdata')    
    path=os.path.join(log_folder,'CCSdata')
    
    files1='\Comodo\Firewall Pro\cisdata.sdb'
    file2='\Comodo\Firewall Pro\cisdata.sdb-shm'
    file3='\Comodo\Firewall Pro\cisdata.sdb-wal'
    
    srcpath1=srcpath+files1
    srcpath2=srcpath+file2
    srcpath3=srcpath+file3
    if  os.path.exists(srcpath1):
        copy(srcpath1,path)
    if  os.path.exists(srcpath2):
        copy(srcpath2,path)
    if  os.path.exists(srcpath3):
        copy(srcpath3,path)
    
def CISdump(srcpath,log_folder):
    print "Copying CCS Dump "    
    path=os.path.join(log_folder,'CCSdump')
    
    srcpath=srcpath+'\Comodo\CisDumps'
    if  os.path.exists(srcpath):
        shutil.copytree(srcpath,path)
    print "CCS Dump file copied"
    
def CISlogs(srcpath,log_folder):
    print "Copying CCS Logs "
    
    os.mkdir(log_folder+'\CCS logs')    
    path=os.path.join(log_folder,'CCS logs')
    srcpath=srcpath+'\Comodo\Firewall Pro\cislogs.sdb'
    if os.path.exists(srcpath):
        copy(srcpath,path)
    print "CCS logs file copied"
    
def CISlogsbackup(srcpath,log_folder): # CIS Log back ups 
    print "Copying CCS Logs Backup "
       
    path=os.path.join(log_folder,'CCS_Logs_Backup')
    srcpath=srcpath+'\Comodo\LogsBackup'
    if  os.path.exists(srcpath):
        shutil.copytree(srcpath,path)
    print "CCS Logs Backup file copied"

    
def AdministrativeEvents(log_folder): # Aminstartive entries 
    print "Copying Administrative Backup "
    os.mkdir(log_folder+'\CCS_Administrative_backups')
    path=os.path.join(log_folder,'CCS_Administrative_backups')
    
    cmd('wevtutil epl System '+path+'\system.evtx')
    cmd('wevtutil epl Application '+path+'\Application.evtx')
    cmd('wevtutil epl  Security '+path+'\Security.evtx')
    cmd('wevtutil epl  Setup '+path+'\Setup.evtx')
        
    print "Administrative Backup  files copied"
    
    
def  Registryconfigurations(log_folder):  # function for registry entries
    print "Registry logs Creatings"
    path=log_folder+r'\configs.reg'
    os.popen('reg export "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CmdAgent\CisConfigs" '+path).read()
    print "Registry logs created"
    
def msiinfo(log_folder): # System info
    os.mkdir(log_folder+'\msiinfo')
    path=os.path.join(log_folder,'msiinfo')
    cmd('msinfo32 /nfo '+path+r"\Msiinfo.nfo")
        
def Versions(log_folder): # version of cis
    os.mkdir(log_folder+'\Version')
    path=os.path.join(log_folder,'Version')
    path1=path+r"\version.txt"
    path2=path+r"\ESmversion.txt"
    f1=open(path1,"w")
    cmd('wmic product get name,version | find "COMODO Client - Security" > '+path1)
    f1.close()
    time.sleep(1)
    f2=open(path2,"w")
    cmd('powershell.exe "get-wmiobject Win32_Product|Format-Table Name,Version" |findstr /i /c:"COMODO Endpoint Security" /c:"COMODO Antivirus for Servers" /c:"COMODO ESM Agent"|sort >'+path2)
    f2.close()
    time.sleep(1)

    
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

def sftp_transfer(winscp_program_path, script_path, file_to_send): ## SFTP Function 
    script_code=r"""
open sftp://c1report:paT7rObeseW0duLl@c1report.comodo.com/ -hostkey=*
cd /reports
put "%s"
close
exit
"""%file_to_send
    with open(script_path, "w") as writer:
        writer.write(script_code)
    transfer_object=Popen('"%s" /script="%s"'%(winscp_program_path, script_path), shell=True, stdout=PIPE, stderr=PIPE)
    transfer_object.communicate()
    return transfer_object.returncode

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
        return '%s\n%s'%(out, err)
            
from os.path import join
import glob

Drivefolder=os.environ['PROGRAMDATA']

main_log_folder=Drivefolder+r'\C1_LOGS'
for filename in glob.glob(main_log_folder):
    if  os.path.exists(main_log_folder):
        shutil.rmtree(filename)
os.mkdir(main_log_folder)
os.chdir(main_log_folder)
time_tag=time.strftime('%Y_%m_%d_%H_%M_%S')
log_folder=main_log_folder+r'\CCS_LOGS'

import sys
import os

if   not os.path.exists(log_folder): ###### Creating  LOG folder
	print "Collecting CCS Logs"
	print "*******"
	os.mkdir(log_folder)
	os.chdir(log_folder)
	srcpath=os.environ['PROGRAMDATA']
	CISdump(srcpath,log_folder)
	CISdata(srcpath,log_folder)
	CISlogs(srcpath,log_folder)
	CISlogsbackup(srcpath,log_folder)
	AdministrativeEvents(log_folder)
	Registryconfigurations(log_folder)
	msiinfo(log_folder)
	Versions(log_folder)
	print "*****"
computer_name=os.getenv('computername')
temp_folder='temp_logs'
path=os.getenv('programdata')

work_directory=os.path.join(path, temp_folder)
ki=os.environ['PROGRAMDATA']
os.chdir(ki)
if os.path.exists(work_directory):
	try:
		shutil.rmtree(work_directory)
		time.sleep(1)    
	except:
		print "You are intiating the script for the second time, Please try again after 15 Minutes"
		import sys
		sys.exit(0)
os.mkdir(work_directory)
## Transfers File

time_tag=time.strftime('%Y_%m_%d_%H_%M_%S')
log_folder2=main_log_folder+r'\CCC_LOGS'
computer_name=os.getenv('computername')

## Collects CCC Logs




if 'PROGRAMW6432' in os.environ.keys():
    main_directory=r"C:\Program Files (x86)\COMODO\Comodo ITSM"
    log_files=[r"C:\Program Files (x86)\COMODO\Comodo ITSM\cdm.db",
               r"C:\Program Files (x86)\COMODO\Comodo ITSM\cdm.db.bck",
               r"C:\Program Files (x86)\COMODO\Comodo ITSM\rmm.dll",
               r'C:\Program Files (x86)\COMODO\Comodo ITSM\pm.db']
    log_folders=[r"C:\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs",
                 r"C:\Program Files (x86)\COMODO\Comodo ITSM\pmlogs",
                 r"C:\Program Files (x86)\COMODO\Comodo ITSM\spmlogs"]
else:
    main_directory=r"C:\Program Files\COMODO\Comodo ITSM"
    log_files=[r"C:\Program Files\COMODO\Comodo ITSM\cdm.db",
               r"C:\Program Files\COMODO\Comodo ITSM\cdm.db.bck",
               r"C:\Program Files\COMODO\Comodo ITSM\rmm.dll",
               r'C:\Program Files\COMODO\Comodo ITSM\pm.db']
    log_folders=[r"C:\Program Files\COMODO\Comodo ITSM\rmmlogs",
                 r"C:\Program Files\COMODO\Comodo ITSM\pmlogs",
                 r"C:\Program Files\COMODO\Comodo ITSM\spmlogs"]
data_logs_folder="C:\\ProgramData\\COMODO\\Comodo ITSM\\logs"

for root, folders, files in os.walk(main_directory):
    for file_name in files:
        
        if file_name.lower().endswith('.dmp'):
            path=os.path.join(root, file_name)
            log_files.append(path)

ccc_log_directory=log_folder2
os.mkdir(ccc_log_directory)
log_files.extend(log_folders)
print "Collecting CCC Logs"
print "***********"
print "copying cdm.db"
print "Copied cdm.db"
print "copyingcdm.db.bck"
print "Copiedcdm.db.bck"
print "copyingrmm.dll"
print "Copiedrmm.dll"
print "copyingrmmlogs"
print "Copiedrmmlogs"
print "copyingpmlogs"
print "Copiedpmlogs"
print "copyingspmlogs"
print "Copiedspmlogs"

for i in log_files:
    copy(i, ccc_log_directory)
if os.listdir(ccc_log_directory):
    print 'Collecting CCC_LOGS %s Done'%('.'*15)
else:
    print 'Failed to Collect CCC_LOGS'
print "*****"
## Transfers File
time_tag=time.strftime('%Y_%m_%d_%H_%M_%S')
c1_file_name='%s_C1_LogData_%s_%s.zip'%(kayako_ticket_number, computer_name, time_tag)
path=os.getenv('PROGRAMDATA')
c1_log_zip_file1=os.path.join(path,c1_file_name)
 
file2=zip_item(main_log_folder, c1_log_zip_file1)
winscp_file_path=os.path.join(work_directory, 'WinSCP_C1_SFTP.exe')
winscp_url=r"https://patchportal.one.comodo.com/portal/packages/spm/DYMO Label Software/x86/WinSCP.exe"
winscp_program_path=download(winscp_url, winscp_file_path)
winscp_script_file=os.path.join(work_directory, 'script_winscp.txt')

if sftp_transfer(winscp_program_path, winscp_script_file,file2)==0:
    print 'Transfering C1_logs %s Done'%('.'*15)
    
else:
    print 'Failed to Transfer CCCLOGs'
os.remove(file2)
ki=os.environ['SYSTEMDRIVE']
os.chdir(ki)

try:
    shutil.rmtree(main_log_folder)
except:
    pass
try:
    shutil.rmtree(work_directory)
except:
    pass
