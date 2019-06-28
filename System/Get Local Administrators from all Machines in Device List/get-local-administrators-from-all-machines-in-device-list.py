Head_computer="STUXNET-PC" #Define here any Computer Name for Generating Reports
emailto='xyz@yopmail.com'### Please edit here to which mail id you want to send report [note: Getter mail id]
emailfrom='xyz123@gmail.com'### please edit here from which mail id you need to get report [note: Sender mail id]
password='abcd123' ###Please edit with the password of sender mail id
smtpserver='smtp.gmail.com'
port=587
import os
import subprocess
import shutil,urllib2,time
from subprocess import PIPE, Popen
import socket
import smtplib
import mimetypes
import ctypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from subprocess import PIPE, Popen
import _winreg
def ipaddress():
    import socket
    return socket.gethostbyname(socket.gethostname())    
def computername():
    import os
    return os.environ['COMPUTERNAME']


def Collectlogs(fileToSend,computer_name):
    s=[]
    Obj = os.popen('net localgroup administrators').read()
    obj1 = os.popen('hostname').read()
    for i in [i.strip() for i in Obj.split('\n')  if i.strip()]:
        s.append(i)
    ki=[]
       
    a=s[4:-1]
    for c, value in enumerate(a, 1):
        i=","+str(c)+" "+value+"\n"
        ki.append(i)
        
	
    b="".join(ki)
    computer_name=computer_name
    fileToSend=os.path.join(os.environ['programdata'],computer_name)
    with open(fileToSend, 'w') as f:
        f.write('Computer Name,Admin users\n')
        f.write(str(obj1))
        f.write(''+str(b))
        f.write('\n')
        f.write('\n')
def Download(Path, URL, FileName,Extension):
    import urllib2
    import os
    fn = FileName + Extension
    fp = os.path.join(Path, fn)
    req = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req)
    with open(fp, 'wb') as f:
        while True:
            chunk=con.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
  
    return fp
    
def computername():
    return os.environ['COMPUTERNAME']
def ipaddress():
    return socket.gethostbyname(socket.gethostname())
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
        return 'The email report has been sent to '+emailto
    except Exception as e:
        return e
def Email(reportfolder,emailto,emailfrom,password,smtpserver,port):
    reportfolder1=reportfolder
    import os
    if os.path.exists(reportfolder):
        ki=os.listdir(reportfolder)
    path=[]
    for i in ki:
        reportfolder=reportfolder1
        path.append(reportfolder+"\\"+i)
        reportfolder=""
           
    with open(reportfolder1+'\\Finalreport.csv' , 'w') as outfile:
        for fname in path:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    msgbody=r'''
    Hi

    Please find the attachment which contains all the device reports 

    Thank you.
    '''
    emailto=emailto
    emailfrom=emailfrom
    password=password
    smtpserver=smtpserver
    port=port
    cf=reportfolder1+'\\Finalreport.csv' 
    subject=' Alldevices report'
    print emailreport(subject,emailto,emailfrom,cf,password,smtpserver,port,msgbody)

def sftp_transfer_mkdir_dele(winscp_program_path, script_path, file_to_send):
    script_code=r"""
open sftp://itsmtemp:aRm5FiOteElysHe9@c1report.comodo.com/ -hostkey=*
cd storage
%s
close
exit
"""%file_to_send
    os.chdir(os.path.join(os.getenv('programdata'),'WInscp_folder'))
    with open(script_path, "w") as writer:
        writer.write(script_code)
    transfer_object=Popen('%s /script="%s"'%("WinSCP_C1_SFTP.exe", script_path), shell=True, stdout=PIPE, stderr=PIPE)
    transfer_object.communicate()
    os.chdir(os.path.join(os.getenv('programdata')))
    return transfer_object.returncode

def sftp_transfer_get(winscp_program_path, script_path):
    script_code=r"""
open sftp://itsmtemp:aRm5FiOteElysHe9@c1report.comodo.com/ -hostkey=*
cd storage
get LocalAdmin
close
exit
"""
    with open(script_path, "w") as writer:
        writer.write(script_code)
    os.chdir(os.path.join(os.getenv('programdata'),'WInscp_folder'))
    transfer_object=Popen('%s /script="%s"'%("WinSCP_C1_SFTP.exe", script_path), shell=True, stdout=PIPE, stderr=PIPE)
    transfer_object.communicate()
    os.chdir(os.path.join(os.getenv('programdata')))
    return transfer_object.returncode    

def sftp_transfer_put(winscp_program_path, script_path, file_to_send):
    script_code=r"""
open sftp://itsmtemp:aRm5FiOteElysHe9@c1report.comodo.com/ -hostkey=*
cd storage
cd LocalAdmin
put "%s" 
close
exit
"""%file_to_send
    with open(script_path, "w") as writer:
        writer.write(script_code)
    os.chdir(os.path.join(os.getenv('programdata'),'WInscp_folder'))
    transfer_object=Popen('%s /script="%s"'%("WinSCP_C1_SFTP.exe", script_path), shell=True, stdout=PIPE, stderr=PIPE)
    os.chdir(os.path.join(os.getenv('programdata')))
    transfer_object.communicate()
    return transfer_object.returncode
work_directory=os.path.join(os.getenv('programdata'),'WInscp_folder')
if os.path.exists(work_directory):
	os.chdir(os.environ['systemdrive'])
	shutil.rmtree(work_directory)
	time.sleep(1)
os.mkdir(work_directory)
computer_name=os.getenv('computername')+'.csv'
log_directory_path=os.path.join(os.environ['programdata'],computer_name)
winscp_file_path=os.path.join(work_directory)
winscp_url=r"https://patchportal.one.comodo.com/portal/packages/spm/DYMO Label Software/x86/WinSCP.exe"
FileName='WinSCP_C1_SFTP'
Extension='.exe'
winscp_program_path=Download( winscp_file_path,winscp_url, FileName,Extension)
Collectlogs(log_directory_path,computer_name)
winscp_script_file=os.path.join(work_directory, 'script_winscp.txt')
string="mkdir LocalAdmin"
sftp_transfer_mkdir_dele(winscp_program_path, winscp_script_file, string)

if sftp_transfer_put(winscp_program_path, winscp_script_file,log_directory_path)==0:
    print 'Transfering File  %s Done'%('.'*15)
else:
    print 'Failed to Transfer file'

computer_name=os.getenv('computername')
if computer_name==Head_computer:
    time.sleep(460)
    if sftp_transfer_get(winscp_program_path, winscp_script_file)==0:
        print 'Downloading File  %s Done'%('.'*15)
    else:
        print 'Downloading failed to Transfer file'
    os.chdir(os.environ['systemdrive'])
    sourcefile=work_directory=os.path.join(os.getenv('programdata'),'WInscp_folder','LocalAdmin')
    destinationfile=os.path.join(os.getenv('programdata'))
    shutil.move(sourcefile,destinationfile)
    string="rm LocalAdmin"
    sftp_transfer_mkdir_dele(winscp_program_path, winscp_script_file, string)
    sourcefile=os.path.join(os.getenv('programdata'),'LocalAdmin')
    Email(sourcefile,emailto,emailfrom,password,smtpserver,port)
    try:
        shutil.rmtree(os.path.join(os.getenv('programdata'),'WInscp_folder'))
    except:
        pass
    if os.path.exists(sourcefile):
        try:
            shutil.rmtree(sourcefile)
        except :
            pass

else:
    print "Report is sent head Computer"
work_directory=os.path.join(os.getenv('programdata'),'WInscp_folder')
try :
    shutil.rmtree(work_directory)
except:
    pass
try :
    os.remove(work_directory)
except:
    pass
try:
    os.remove(log_directory_path)
except :
    pass
print "For your Information:"
print "Make Sure you Defined Head Computer"
