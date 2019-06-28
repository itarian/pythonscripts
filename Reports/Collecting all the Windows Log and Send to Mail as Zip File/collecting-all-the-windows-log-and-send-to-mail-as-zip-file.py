zip_fname=r'Windows_Logs.zip'           #Give the name for your Output Zip file

emailto=['abc@yopmail.com']             # Provide an email where want to send Output zip file.
emailfrom='xyz@gmail.com'               # Provide a valide from email.
password='*********'	                # Provide the correct password for your from mail.
smtpserver='smtp.gmail.com'
port=587



sendmail=1 ## [1 sends mail or 0 does not send mail] if sendmail=1 then user have to set the required information to send out a email from the code.
msgbody=r'''Hi

Please find the attachment for the Windows Logs in zip file format.

Thank you.'''


import os
import ctypes
import zipfile
import shutil
import re
import random
import socket
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

def computername():
    return os.environ['COMPUTERNAME']

def ipaddress():
    return socket.gethostbyname(socket.gethostname())

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
            
workdir=os.environ['PROGRAMDATA']+r'\c1_temp\Win_Logs'
if not os.path.exists(workdir):
    os.makedirs(workdir)

def logs():
    print "Collecting Windows Logs\n"
    for i in range(1,5):
        i=str(i)
        with disable_file_system_redirection():
            c='wevtutil qe System '+'"'+"/q:*[System [(Level="+i+")]]"+'"'+" /f:text /rd:True > " +workdir+'\Logs'+i+'.txt'
            os.popen(c)
            

def zip_item(path, zip_file_path):  # Creating ZIP file
    print "Zipping up the Log folder\n"

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
    

def rename():
    os.rename('C:\ProgramData\c1_temp\Win_Logs\Logs1.txt', 'C:\ProgramData\c1_temp\Win_Logs\Critical_events.txt')
    os.rename('C:\ProgramData\c1_temp\Win_Logs\Logs2.txt', 'C:\ProgramData\c1_temp\Win_Logs\Error_events.txt')
    os.rename('C:\ProgramData\c1_temp\Win_Logs\Logs3.txt', 'C:\ProgramData\c1_temp\Win_Logs\Warning_events.txt')
    os.rename('C:\ProgramData\c1_temp\Win_Logs\Logs4.txt', 'C:\ProgramData\c1_temp\Win_Logs\Information_events.txt')
    
    

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
        shutil.copytree(source_path, destination_folder)
        return destination_folder

def emailreport(subject, emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody):
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ",".join(emailto)
    msg["Subject"] = subject
    msg.preamble = subject
    body = MIMEText(msgbody)
    msg.attach(body)       
    with open(fileToSend, 'rb') as fp:
        record = MIMEBase('text', 'octet-stream')
        record.set_payload(fp.read())
        encoders.encode_base64(record)
        record.add_header('Content-Disposition', 'attachment', filename=os.path.basename(fileToSend))
        msg.attach(record)
    try:
        server = smtplib.SMTP(smtpserver,port)
        server.ehlo()
        server.starttls()
        server.login(emailfrom, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        return "The email report has been sent to "+msg["To"]
    except Exception as e:
        return e


def remove():
    shutil.rmtree(workdir)
    shutil.rmtree(work_directory)
    
logs()
rename()


temp_folder='Windows_Logs'
work_directory=os.path.join(os.getenv('temp'), temp_folder)
if os.path.isdir(work_directory):
    shutil.rmtree(work_directory)
os.mkdir(work_directory)
log_files=[r"C:\ProgramData\c1_temp\Win_Logs\Critical_events.txt",
               r"C:\ProgramData\c1_temp\Win_Logs\Error_events.txt",
               r"C:\ProgramData\c1_temp\Win_Logs\Warning_events.txt",
               r"C:\ProgramData\c1_temp\Win_Logs\Information_events.txt"]

for i in log_files:
    path=copy(i,work_directory)

zip_name=os.path.join(os.getenv('temp'),zip_fname )
path=zip_item(work_directory,zip_name)

fileToSend=os.path.join(os.getenv('temp'),zip_fname )
subject='%s %s Windows Logs as Zip'%(computername(), ipaddress())
if sendmail==1:
    print emailreport(subject,emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody)
else:
    print "Make send mail value as 1"


remove()
