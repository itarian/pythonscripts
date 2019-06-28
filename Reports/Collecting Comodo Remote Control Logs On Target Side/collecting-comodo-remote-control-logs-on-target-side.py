kayako_ticket_number="xxxxxxxx"
import urllib2
import os
import shutil
import zipfile
import time
import ctypes
from subprocess import PIPE, Popen

def copy(source_path, destination_path):  # Copy Function
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
            print source_path + " Doesnt Exist"
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
work_directory=os.path.join(os.getenv('PROGRAMDATA'), temp_folder)
if os.path.isdir(work_directory):
    try:
        shutil.rmtree(work_directory)
    except:
        sys.exit(0)
os.mkdir(work_directory)
log_directory_path=os.path.join(work_directory, 'log_directory')
os.mkdir(log_directory_path)

## Collects CRC Logs
time_tag=time.strftime('%Y_%m_%d_%H_%M_%S')
c1_file_name='%s_CRCLog-TargetSide_%s_%s.zip'%(kayako_ticket_number, computer_name, time_tag)
c1_log_zip_file=os.path.join(work_directory, c1_file_name)

if 'PROGRAMW6432' in os.environ.keys():
    main_directory=r"C:\Program Files (x86)\COMODO\Comodo ITSM"
    log_files=[r"C:\Program Files (x86)\COMODO\Comodo ITSM\cdm.db",
               r"C:\Program Files (x86)\COMODO\Comodo ITSM\remoting.daemon.log",
               r"C:\Program Files (x86)\COMODO\Comodo ITSM\remoting.desktop.log",
               r'C:\Program Files (x86)\COMODO\Comodo ITSM\remoting.host.log']
 
else:
    main_directory=r"C:\Program Files\COMODO\Comodo ITSM"
    log_files=[r"C:\Program Files\COMODO\Comodo ITSM\cdm.db",
               r"C:\Program Files\COMODO\Comodo ITSM\remoting.daemon.log",
               r"C:\Program Files\COMODO\Comodo ITSM\remoting.desktop.log",
               r'C:\Program Files\COMODO\Comodo ITSM\remoting.host.log']

print "Collecting CRC Logs"
crc_log_directory=os.path.join(log_directory_path, 'crc_logs')
if os.path.exists(crc_log_directory):
    sys.exit(0)
os.mkdir(crc_log_directory)
for i in log_files:
    path=copy(i,crc_log_directory)
path=zip_item(log_directory_path,c1_log_zip_file)
print "Zip file created to" +(c1_log_zip_file)
if os.listdir(crc_log_directory):
    print 'Collecting CRCLOGS on Target Side %s Done'%('.'*15)
else:
    print 'Failed to Collect CRCLOGS on Target Side'
ki=os.environ['TEMP']
winscp_file_path=os.path.join(work_directory, 'WinSCP_C1_SFTP.exe')
winscp_url="https://patchportal.one.comodo.com/portal/packages/spm/DYMO%20Label%20Software/x86/WinSCP.exe"
app="WinSCP_C1_SFTP.exe"
winscp_program_path=download(winscp_url, winscp_file_path)
winscp_script_file=os.path.join(work_directory, 'script_winscp.txt')
if sftp_transfer(winscp_program_path, winscp_script_file,path)==0:
    print 'Transfering CRCLOGs %s Done'%('.'*15)
    
else:
    print 'Failed to Transfer CRCLOGs'
try:
    shutil.rmtree(work_directory)
except:
    pass
try:
	shutil.rmtree(log_directory_path)
except:
	pass

try:
    shutil.rmtree(crc_log_directory)
except:
    pass
