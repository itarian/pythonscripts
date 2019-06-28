#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('variableName') with that parameter's name
emailto='tamil111@yopmail.com' #To define a particular receiver email address here
import os
import subprocess
from subprocess import PIPE, Popen
import re
import shutil


def ipaddress():
    import socket
    return socket.gethostbyname(socket.gethostname())    
def computername():
    import os
    return os.environ['COMPUTERNAME']
try:
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)      
except:
    workdir=os.environ['SYTEMDRIVE']


    
bat_file=workdir+r'Bat_file.bat'
check=['0','90','7','1','4']

content='''start cmd.exe /c "secedit /export /cfg C:\\ProgramData\\temp\\group-policy.inf /log export.log"
'''

with open(bat_file, 'wb') as fr:
    fr.write(content)

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
                            "Subject": "Status of the Password Policy ",
                            "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
                            "HTMLPart": """<h3> Hi

        Please find the attachment which contains the Status of the Password Policy

        Thank you.</h3>""",
                            "Attachments": [
                                    {
                                            "ContentType": "text/csv",
                                            "Filename": "group-policy.csv",
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
            print "Email has been Sent Successfully to the following mail adddress :",'"'+emailto+'"'
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

def remove():
    try:
        os.remove("C:\\ProgramData\\temp\\group-policy.inf")
        os.remove('C:\\ProgramData\\temp\\test.txt')
        os.remove(path)
        
    except:
        pass   

obj = subprocess.Popen(bat_file, shell = True, stdout = PIPE, stderr = PIPE)
out, err = obj.communicate()
print err
path="C:\\ProgramData\\temp\\group-policy.csv"
if os.path.isfile("C:\\ProgramData\\temp\\group-policy.inf"):
    with open("C:\\ProgramData\\temp\\group-policy.inf",'r') as f:
        with open('C:\\ProgramData\\temp\\test.txt','w+') as wr:
            k= f.read().decode('utf-16')
            k1=wr.write(k)
            
    with open("C:\\ProgramData\\temp\\test.txt",'r') as f:
        k=f.readlines()[3:8]
    header=[]
    value=[]
    for i in k:
        header.append(i.split('=')[0].strip())
        value.append(i.split('=')[1].replace('\n','').strip())
        
    header=list(filter(None, header))
    value=list(filter(None, value))
    if header and value:
        with open(path,'w+') as wr:
            wr.write("\t\tPASSWORD GROUP  POLICIES :\n\n")
            wr.write('COMPUTER NAME,'+str(computername()))
            wr.write('\nIP ADDRESS,'+str(ipaddress()))
            wr.write('\n\n\n')
            for i in header:
                wr.write(unicode(str(i)+',').encode('utf-8'))
            wr.write('\n')
            for i in value:
                wr.write(unicode(str(i)+',').encode('utf-8'))
            wr.write('\n\n\n')
            if check[0]==value[0]:
                
                wr.write(str("\n\nMinimum Password age is defined as ".upper()+','+check[0]))
            else:
                wr.write (str("\n\nMinimum Password age is not defined as ".upper()+','+check[0]))
            if check[1]==value[1]:
                wr.write (str("\n\nMaximum Password age is defined as ".upper()+','+check[1]))
            else:
                wr.write (str("\n\nMaximum Password age is not defined as ".upper()+','+check[1]))
            if check[2]==value[2]:
                wr.write (str("n\nMinimum Password length is defined as ".upper()+','+check[2]))
            else:
                wr.write (str("\n\nMinimum Password length is not defined as ".upper()+','+check[2]))
            if check[3]==value[3]:
                wr.write (str("\n\nPassword complexity is enabled ".upper()+','+check[3]))
            else:
                wr.write (str("\n\nPassword complexity is not enabled ".upper()+','+check[3]))
            if check[4]==value[4]:
                wr.write (str("\n\nPassword History Size is Maintained as ".upper()+','+check[4]))
            else:
                wr.write (str("\n\nPassword History Size is not Maintained as ".upper()+','+check[4]))
else:
    print "Could not create Group policy file in specified directory"

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
    print "Password Policy Report has been successfully created\n"
    Email(path,emailto)
    remove()

else:
    print "Password Policy Report has been successfully created"

