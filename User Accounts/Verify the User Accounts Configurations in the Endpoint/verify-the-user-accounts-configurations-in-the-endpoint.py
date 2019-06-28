
emailto='tamil123@yopmail.com' #To define a particular receiver email address here
max_login_attempt=8         #please Mention the Maximun number of incorrect attempts in device password
lockout_duration=35         #please Mention the lockout duration is set to a minimum of number of minutes 
auto_lock_accounts=20       #please Mention the Auto lock set to lock after a maximum of  number of minutes 
unique_initial_password=6   #please Mention the new accounts are set with a unique initial password && The remebered password must be wiithin the range of (1-24)

import os
import subprocess
from subprocess import PIPE, Popen
import re
import shutil


try:
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)      
except:
    workdir=os.environ['SYTEMDRIVE']



def Email(fileToSend,To):
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
                            "Subject": "USER ACCOUNTS  CONFIGURATIONS IN THE ENDPOINT\n",
                            "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
                            "HTMLPart": """<h3> Hi

        Please find the attachment which contains the USER ACCOUNTS  CONFIGURATIONS IN THE ENDPOINT

        Thank you.</h3>""",
                            "Attachments": [
                                    {
                                            "ContentType": "text/csv",
                                            "Filename": "verifyaccounts.csv",
                                            "Base64Content": "%s"%ki
                                    }
                            ]
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    ret=result.status_code
    if ret==200:
        out=result.json()
        out=str(out)
        if "success" in out:
            print "Email has been Sent Successfully to the following mail address:"+' "'+emailto+'"'
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

def remove(path):
    try:
        os.remove(path)     
    except:
        pass

def ipaddress():
    import socket
    return socket.gethostbyname(socket.gethostname())    
def computername():
    import os
    return os.environ['COMPUTERNAME']


 
import os
path=os.path.join(os.environ['programdata'],'verifyaccounts.csv')
f=open(path,'w+')
f.write(',USER ACCOUNTS  CONFIGURATIONS IN THE ENDPOINT\n\n\n')
f.write('COMPUTER NAME,'+str(computername()))
f.write('\n')
f.write('\nIP ADDRESS,'+str(ipaddress()))
f=open(path,'a+')
def lockout():
    f.write('\n\nLOCKOUT CHECK:')
    f.write('\n')
    x=[]
    k=os.popen('wmic useraccount get name,Lockout').read().split('\r\n')
    for i in k:
        if 'TRUE' in i:
            x.append(i.split()[-1])
    
    if x:
        f.write('\n,The following accounts are Locked in the Endpoint:\n')
        f.write('\n')
        for i in x:
            f.write(i)
            f.write('\n')
            

    else:
        f.write('\n')
        f.write('\n,No accounts are Locked in the Endpoint\n')

    f.write('\n\n\n')
    
def login():
    f.write('\nFIRST LOGIN CHECK:')
    f.write('\n')
    x1=[]
    x2=[]
    k1=os.popen('wmic useraccount get name,PasswordExpires').read().split('\r\n')
    for i in k1:
        if 'TRUE' in i:
            x1.append(i.split()[0])
        if 'FALSE' in i:
            x2.append(i.split()[0])
    if x1:
        f.write('\n,The following accounts are having the option of resetting their password on the first login in the Endpoint:\n')
        for i in x1:
            f.write('\n,'+'*)'+i)
            f.write('\n')
        f.write('\n\n')
    if x2:
        f.write('\n,The following accounts are not having the option of resetting their password on the first login in the Endpoint:\n')
        for i in x2:
            f.write('\n,'+'*)'+i)
            f.write('\n')
        f.write('\n\n')
    else:
        f.write('\n,No accounts having the reset their password on the first login in the Endpoint\n')
        f.write('\n\n')


    f.write('\n\n\n')



def unique():
    f.write('\nUNIQUE INIATIL PASSWORD CHECK:')
    f.write('\n')
    uni=os.popen('net accounts | findstr /i: history').read()
    if 'None' in uni.split(':')[-1].strip():
        f.write('\n,'+uni.split(':')[0].strip()+','+uni.split(':')[-1].strip())
        f.write('\n')
        f.write('\n,There is no Unique Initial Password Remebered\n')

        
    else:
        if int(uni.split(':')[-1].strip()) == unique_initial_password:
            f.write('\n,'+uni.split(':')[0].strip()+','+uni.split(':')[-1].strip())
            f.write('\n')
            f.write('\n,Unique password attempt is already set to maximum of %d incorrect attempts\n'%unique_initial_password)

        else:
            f.write('\n,'+uni.split(':')[0].strip()+','+uni.split(':')[-1].strip())
            f.write('\n')
            f.write('\n,Unique password attempt is Not set to maximum of %d incorrect attempts\n\n'%unique_initial_password)
    f.write('\n\n\n')
    
def maxlockout():
    f.write('\nMAXIMUM LOGIN ATTEMPT CHECK:')
    f.write('\n')
    lkt=os.popen('net accounts | findstr /i: threshold').read()
    if 'Never' in lkt.split(':')[-1].strip():
        f.write('\n,'+lkt.split(':')[0].strip()+','+lkt.split(':')[-1].strip())
        f.write('\n')
        f.write('\n,There is no Lockout threshold in the account\n')


    else:
        if int(lkt.split(':')[-1].strip()) == max_login_attempt:
            f.write('\n,'+lkt.split(':')[0].strip()+','+lkt.split(':')[-1].strip())
            f.write('\n')
            f.write('\n,Lockout Threshold attempt is already set to the maximum of %d incorrect attempts\n'%max_login_attempt)

        else:
            f.write('\n,'+lkt.split(':')[0].strip()+','+lkt.split(':')[-1].strip())
            f.write('\n')
            f.write('\n,Lockout Threshold attempt is not set to the maximum of %d incorrect attempts\n'%max_login_attempt)
    
def maxlockduration():
    f.write('\nLOCKOUT DURATION CHECK:')
    f.write('\n')
    lkd=os.popen('net accounts | findstr /i: duration').read()
    if int(lkd.split(':')[-1].strip()) == lockout_duration :
        f.write('\n'+','+lkd.split(':')[0].strip()+','+lkd.split(':')[-1].strip())
        f.write('\n')
        f.write('\n,Lockout duration is already set to the minimum of %d minutes\n'%lockout_duration)

    else:
        f.write('\n'+','+lkd.split(':')[0].strip()+','+lkd.split(':')[-1].strip())
        f.write('\n')
        f.write('\n,Lockout duration is not set to the minimum of %d minutes\n'%lockout_duration)
        

    
    f.write('\n\n\n')
def autolock():
    f.write('\nLOCK AFTER MAXIMUM DURATION CHECK:')
    f.write('\n')
    lko=os.popen('net accounts | findstr /i: observation').read()
    if int(lko.split(':')[-1].strip()) == auto_lock_accounts:
        f.write('\n'+','+lko.split(':')[-0].strip()+','+lko.split(':')[-1].strip())
        f.write('\n')
        f.write('\n,Auto Lockout window is already set to lock after a maximum of %d minutes\n'%auto_lock_accounts)

        
    else:
        f.write('\n'+','+lko.split(':')[-0].strip()+','+lko.split(':')[-1].strip())
        f.write('\n')
        f.write('\n,Auto Lockout window is not set to lock after a maximum of %d minutes\n'%auto_lock_accounts)
    f.write('\n\n\n')

    
lockout()
maxlockout()
maxlockduration()
autolock()
unique()
login()
f.close()
print "USER ACCOUNTS  CONFIGURATIONS IN THE ENDPOINT WAS COLLECTED SUCCESSFULLY AND READY SEND VIA EMAIL\n"
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
if os.path.exists(path):
    Email(path,emailto)
    remove(path)

else:
    print 'Could not Fetch the USER ACCOUNTS CONFIGURATIONS IN THE ENDPOINT'
