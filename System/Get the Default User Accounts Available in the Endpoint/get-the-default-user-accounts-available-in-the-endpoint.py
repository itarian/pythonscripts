#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('variableName') with that parameter's name
emailto='tamil12@yopmail.com' #To define a particular receiver email address here
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
                            "Subject": "List of Defalut User Accounts",
                            "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
                            "HTMLPart": """<h3> Hi

        Please find the attachment which contains the List of Defalut User Accounts

        Thank you.</h3>""",
                            "Attachments": [
                                    {
                                            "ContentType": "text/csv",
                                            "Filename": "accounts.csv",
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
            print "Email has been Sent Successfully to the following mail address :"+' "'+emailto+'"'
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

path=os.path.join(os.environ['programdata'],'accounts.csv')                  
cmd='wmic useraccount get name /format:csv > %s'%path
os.popen(cmd).read()
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
    print "List of Defalut User Accounts Report has been successfully created\n"
    Email(path,emailto)
    remove(path)

else:
    print 'Could not Fetch the List of Defalut User Accounts'
