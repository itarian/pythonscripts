Head_computer=r"DESKTOP-AUMJTHF" #Define here any Computer Name for Generating Reports
emailto='tamil@yopmail.com'#you need to Give Your Email for Getting reports
Fn="plogs" #you need mention your report file name 
emailfrom='logtestcomodoscripts@gmail.com'
password='Passw0rd!@123'
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
def osname():
    import re
    d=os.popen('systeminfo').read()
    get=re.findall('OS Name:(.*)',d)
    s=''.join(get).strip()
    return s

def Collectlogs(fileToSend,computer_name):
    import os
    import re
    import shutil
    import random
    drive=os.environ['SYSTEMDRIVE']
    if  'PROGRAMW6432' in os.environ.keys():
        spmpath=drive+r'\Program Files (x86)\COMODO\Comodo ITSM\spmlogs'
        pmlpath=drive+r'\Program Files (x86)\COMODO\Comodo ITSM\pmlogs'
    else:
        spmpath=drive+r'\Program Files\COMODO\Comodo ITSM\spmlogs'
        pmlpath=drive+r'\Program Files\COMODO\Comodo ITSM\pmlogs'
    lin=""
    col=[]
    colu=[]
    update=os.environ['temp']
    update1=update+'\\'+'templogs.txt'
    
    update2=update+'\\'+'SPM_LOGS.txt'
    update3=update+'\\'+'LOGS_REPORT.txt'
    tempd=update+'\\'+'tempPM.txt'
    templ=update+'\\'+'templogs_PM.txt'
    
    
    logfiles=[os.path.join(spmpath, i) for i in os.listdir(spmpath) if i.startswith('SpmAgent.log')]

    print "Collecting SPM reports\n"
    with open(update1,'w') as w:
       for i in logfiles:
           with open (i,'rb') as r:
               w.write(r.read())

    with open(update1,'r') as wt:
        for i in wt:
            if 'BEGIN SUPPORTED SOFTWARE LIST' in i:
                
                col.append(i)

    with open(update1,'r') as wt:
        with open(update2, 'w') as et:
            le=len(col)
            
            ch=str(col[le-1])
            
            for i in wt:
                if ch in i:
                    et.write(i)
                    for i in wt:

                        if not "END SUPPORTED SOFTWARE LIST" in i:
                            if "displayName:" in i:
                                et.write(i)
                        else:
                            et.write(i)
                            et.write('\n\n')
                            break

            
    with open(update1,'r') as wt:
        for i in wt:
            if 'BEGIN UNSUPPORTED SOFTWARE LIST' in i:
                
                colu.append(i)

    with open(update1,'r') as wt:
        with open(update2, 'a+') as et:
            le=len(colu)
            
            ch=str(colu[le-1])
            
            for i in wt:
                if ch in i:
                    et.write(i)
                    for i in wt:

                        if not "END UNSUPPORTED SOFTWARE LIST" in i:
                            if "displayName:" in i:
                                et.write(i)
                        else:
                            et.write(i+'\n\n')
                            break
                        
    cn=computername()
    ip=ipaddress()
    with open(update2, 'r+') as dr:
        with open(fileToSend, 'w+' ) as de:
                de.write('COMPUTER NAME:'+cn+'\n')
                de.write('IP ADDRESS:'+ip+'\n')
                de.write("\t\t\t\t\t\t\t\t\tTHIRD PARTY APPLICATION INFO" +'\n\n')
                k=''
                c=re.findall('===(.*)|"(.*)"',dr.read())
                for i in c:
                    k=''.join(i).strip()
                    de.write(k+'\n')
                

        
    print "Successfully collected SPM logs\n"
    logfiles=[os.path.join(pmlpath, i) for i in os.listdir(pmlpath) if i.startswith('PmAgent.log')]
    print "Collecting PM Logs\n"
    with open(tempd, 'wb') as w:        
        for i in logfiles:
            with open(i, 'rb') as r:
                 w.write(r.read())

    with open(templ, 'w') as w:
        with open(tempd) as r:
            while True:
                line=r.readline()
                if line:
                    if 'Metadata' in line or 'Title:' in line or 'Patch Primary Category: "Security Updates"' in line or 'Patch Primary Category: "Critical Updates"' in line:
                        w.write(line)
                else:
                    break


    
    with open(templ) as fr:
        with open(fileToSend, 'a+') as c1:
            c1.write("\n \t\t\t\t\t\t\t\t\tOS PATCHES INFORMATION\n\n")

            for i in re.findall('Title:.*\n.*Updates"',fr.read()):
                ob=re.search('".*\(.*\)"', i)
                if ob:
                    t1=ob.group()
                    if t1:
                        c1.write(t1[1:-1]+'\n')
            c1.write("************************************************************************************************************************************************\n\n")

    os.remove(templ)
    os.remove(tempd)
    os.remove(update1)
    os.remove(update2)
  
        

    print "Successfully collected PM logs\n"
    print "ITSM LOGS ARE SUCCESSFULLY COLLECTED"
    
   
def download(url, file_path):
    url_object=urllib2.urlopen(url)
    download_data=url_object.read()
    with open(file_path, "wb") as writer:
        writer.write(download_data)
    return file_path
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
        return "The email report has been sent to "+msg["To"]
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
           
    with open(reportfolder1+'\\'+Fn+'.txt' , 'w') as outfile:
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
    cf=reportfolder1+'\\'+Fn+'.txt' 
    subject=' Alldevices ITSM PATCH report'
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
get %s
close
exit
"""%Fn
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
cd %s
put "%s" 
close
exit
"""%(Fn,file_to_send)
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
computer_name=os.getenv('computername')+".txt"
log_directory_path=os.path.join(os.environ['temp'],computer_name)
winscp_file_path=os.path.join(work_directory, 'WinSCP_C1_SFTP.exe')
winscp_url=r"https://patchportal.one.comodo.com/portal/packages/spm/DYMO Label Software/x86/WinSCP.exe"
winscp_program_path=download(winscp_url, winscp_file_path)
Collectlogs(log_directory_path,computer_name)
winscp_script_file=os.path.join(work_directory, 'script_winscp.txt')
string="mkdir %s"%Fn
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
    sourcefile=work_directory=os.path.join(os.getenv('programdata'),'WInscp_folder',Fn)
    destinationfile=os.path.join(os.getenv('programdata'))
    shutil.move(sourcefile,destinationfile)
    string="rm %s"%Fn
    sftp_transfer_mkdir_dele(winscp_program_path, winscp_script_file, string)
    sourcefile=os.path.join(os.getenv('programdata'),Fn)
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
    print "Report is sent Head Computer"
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
