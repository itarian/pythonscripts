emailto='************'  # Enter an email where want to get an email. 

import os
import re
import ctypes
import getpass
import time
import subprocess
from subprocess import PIPE, Popen
import sys
import difflib

cmd_off='wevtutil qe Security "/q:*[System [(EventID=4634)]]" /rd:true /f:text /c:1'
cmd_on='wevtutil qe Security "/q:*[System [(EventID=4624)]]" /rd:true /f:text /c:1'
Date=[]
Time=[]
Acc_name=[]
Date1=[]
Time1=[]
Acc_name1=[]
flag=0

Device=str(os.environ['COMPUTERNAME'])


try:
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)      
except:
    workdir=os.environ['SYTEMDRIVE']

New_ON=workdir+r"\New_LogOn.txt"
New_Off=workdir+r"\New_LogOff.txt"
Old_ON=workdir+r"\Old_LogOn.txt"
Old_Off=workdir+r"\Old_LogOff.txt"
File_To_Send=workdir+r"\Report.txt"




def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))

   
def command(cmd):        
    obj = subprocess.Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    print err
    return out

def logon(file0):
    out=command(cmd_on)
    if out:
        user=getpass.getuser()
        if "$" in user:
            pass
        else:
            Acc_name.append("Account Name : "+user)
            gt=re.findall('Date:(.*)', out)
            date=re.findall('(.*)T', gt[0])
            Date.append("Log_On Date : "+date[0].strip())
            time=re.findall('T(.*)', gt[0])
            Time.append("Log_On Time : "+time[0].strip())
            with open(file0, 'w+') as fr:
                fr.write(str(Acc_name[0])+"\n")
                fr.write(str(Date[0])+"\n")
                fr.write(str(Time[0])+"\n")
    else:
        print "\nFailed to retrieve LOG_ON details\n"


def logoff(file1):
    out=command(cmd_off)
    if out:
        gl=re.findall('Account Name:(.*)', out)
        if "$" in gl[0]:
            pass
        else:
            Acc_name1.append("Account Name : "+gl[0].strip())
            gt=re.findall('Date:(.*)', out)
            date=re.findall('(.*)T', gt[0])
            Date1.append("Log_Off Date : "+date[0].strip())
            time=re.findall('T(.*)', gt[0])
            Time1.append("Log_Off Time : "+time[0].strip())
            with open(file1, 'w+') as fr:
                fr.write(str(Acc_name1[0])+"\n")
                fr.write(str(Date1[0])+"\n")
                fr.write(str(Time1[0])+"\n")

    else:
        print "\nFailed to retrieve LOG_OFF details\n"


def prnt():
    with open(File_To_Send, 'a+') as dr:
        with open(New_ON, 'r') as de:
            for i in de:
                dr.write(i)
        dr.write("\n")
    print "\n"

    with open(File_To_Send, 'a+') as dr:
        with open(New_Off, 'r') as de:
            for i in de:
                dr.write(i)



def Email(fileToSend,To,Device):
    from mailjet_rest import Client
    import os
    api_key='3e70858a7a5c5fbc245a662d5d9aa238'   # API KEY of Mail Jet 
    api_secret= 'a337abcc84d8fb062f6f1597d966ae6f'  # API SECRET KEY of Mail Jet
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    import base64
    with open(fileToSend, 'rb') as fp:
        ki=base64.b64encode(fp.read())
    data = {
      'Messages': [
                    {
                            "From": {
                                    "Email": "c1operations123@gmail.com",
                            },
                            "To": [
                                    {
                                            "Email": "%s"%To,
                                    }
                            ],
                            "Subject": "Logging Details for the device %s account name is  %s "%(Device,kp),
                            "TextPart": "Please find the last Logging details of user. \n%s"%cont1
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    ret=result.status_code
    if ret==200:
        out=result.json()
        out=str(out)
        if "success" in out:
            print "Report Email Sent Successfully"
    else:
        print "Error sending email"

def zip_item(path,final_path):  # Creating ZIP file
    import zipfile
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(final_path)
    zip_ref.close()
    return final_path


def Download(URL, DownloadTo = None, FileName = None):
    import urllib
    import ssl
    if FileName:
        FileName = FileName
    else:
        FileName = URL.split('/')[-1]
        
    if DownloadTo:
        DownloadTo = DownloadTo
    else:
        DownloadTo = os.path.join(os.environ['TEMP'])
        
    DF = os.path.join(DownloadTo, FileName)
    with open(os.path.join(DownloadTo, FileName), 'wb') as f:
        try:
            context = ssl._create_unverified_context()
            f.write(urllib.urlopen(URL,context=context).read())
        except:
            f.write(urllib.urlopen(URL).read())
    if os.path.isfile(DF):
        return DF
    else:
        return False

    
def mailjet(DEST):
    BDPATH = Download(r'https://drive.google.com/uc?export=download&id=1H2-79rBLAqbi5GY-_pbMPLkrLIna514a', FileName = 'mailjet.zip')
    SRC = os.path.join(os.environ['TEMP'])
    path=zip_item(BDPATH,SRC)
    SRC = os.path.join(os.environ['TEMP'],'mailjet')
    from distutils.dir_util import copy_tree
    copy_tree(SRC, DEST) 
        
def to_alert(Old_ON, Old_Off, New_ON, New_Off):
    flag=0
    with open(Old_ON) as file:
        data=file.read()
        with open(New_ON) as file:
                data2=file.read()
                text1Lines = data.splitlines(1)
                text2Lines = data2.splitlines(1)
                diffInstance = difflib.Differ()
                diffList = list(diffInstance.compare(text1Lines,text2Lines ))
                for line in diffList:
                        if line[0] == '+':
                                flag=1

    with open(Old_Off) as file:
        data=file.read()
        with open(New_Off) as file:
                data2=file.read()
                text1Lines = data.splitlines(1)
                text2Lines = data2.splitlines(1)
                diffInstance = difflib.Differ()
                diffList = list(diffInstance.compare(text1Lines,text2Lines ))
                for line in diffList:
                                    if line[0] == '+':
                                            flag=1

    return flag
           
def file_change():
    open(workdir+r"\count.txt", 'a').close()
    os.rename(workdir+r"\New_LogOn.txt",workdir+r"\Old_LogOn.txt" )
    os.rename(workdir+r"\New_LogOff.txt",workdir+r"\Old_LogOff.txt" )
    os.remove(File_To_Send)
    

def rem_change():
    os.remove(workdir+r"\Old_LogOn.txt")
    os.remove(workdir+r"\Old_LogOff.txt")
    os.rename(workdir+r"\New_LogOn.txt",workdir+r"\Old_LogOn.txt" )
    os.rename(workdir+r"\New_LogOff.txt",workdir+r"\Old_LogOff.txt" )
    if os.path.isfile(File_To_Send):
        os.remove(File_To_Send)
    

def txt_send():
    with open(File_To_Send, 'r') as rr:
            contents =rr.read()
            c1=re.findall("Account Name :(.*)",contents)
            c2=set(c1)
            c3=list(c2)
            kk=', '.join(c3)
            return kk,contents
            
            
    
HOMEPATH = r"C:\Program Files (x86)"
if os.path.exists(HOMEPATH):
        HOMEPATH = r"C:\Program Files (x86)"
else:
    HOMEPATH =r"C:\Program Files"

DEST= os.path.join(HOMEPATH,r'COMODO\Comodo ITSM\Lib\site-packages')
Folders=os.listdir(DEST)
Nodow=0
Del_folders=['mailjet-1.4.1-py2.7.egg-info', 'mailjet_rest', 'mailjet_rest-1.3.0-py2.7.egg-info']
for i in Del_folders:
    if i in Folders:
        Nodow=Nodow+1
if Nodow>2:
    c=0
else:
    DEST=mailjet(DEST)

if os.path.isfile(workdir+r"\count.txt"):
    logon(New_ON)
    logoff(New_Off)
    val=to_alert(Old_ON, Old_Off, New_ON, New_Off)

    if val>0:
        print "\nNew User has logged in or Logged off within the time interval.Please check mail for details.\n"
        prnt()
        kp,cont1=txt_send()
        Email(File_To_Send,emailto,Device)
        alert(1)
    else:
        alert(0)
        print "\nNo User has logged in or Logged off within the time interval.\n"
    rem_change()
else:
    print "Running this procedure for the first time in this Endpoint."
    logon(New_ON)
    logoff(New_Off)
    prnt()
    kp,cont1=txt_send()
    
    if os.path.isfile(File_To_Send):
        Email(File_To_Send,emailto,Device)
    else:
        print "Failed to generate report file to send to mail\n"
    file_change()
    alert(1)
