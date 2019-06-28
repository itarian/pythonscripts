#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('variableName') with that parameter's name
emailto=itsm.getParameter('Email_ID')
import os
import sys
import shutil
import zipfile
from distutils.dir_util import copy_tree
def Email(fileToSend,To):
    from mailjet_rest import Client
    import os
    filename=os.environ['COMPUTERNAME']+r'.zip'
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
                            "Subject": "ITSM Monitoring ,Procedure and Patch Management logs Report",
                            "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
                            "HTMLPart": """<h3> Hi

        Please find the attachment which contains the report of ITSM Monitoring ,Procedure and Patch Management logs Report


        Thank you.</h3>""",
                            "Attachments": [
                                    {
                                            "ContentType": "text/zip",
                                            "Filename": "%s"%filename,
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
            print "Email sent successfully"
            return 0
    else:
        print "Error sending email"
        return 1
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
    os.chdir(DownloadTo)
    DF=os.path.join(os.environ['TEMP'],FileName)
    with open(FileName, 'wb') as f:
        try:
            context = ssl._create_unverified_context()
            f.write(urllib.urlopen(URL,context=context).read())
        except:
            f.write(urllib.urlopen(URL).read())
    if os.path.isfile(DF):
        return DF
    else:
        return False
def zip_item(path,final_path):  # Creating ZIP file
    import zipfile
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(final_path)
    zip_ref.close()
    return final_path
def Import_pubnub(DEST):
    BDPATH = Download(r'https://drive.google.com/uc?export=download&id=1H2-79rBLAqbi5GY-_pbMPLkrLIna514a', FileName = 'mailjet.zip')
    SRC = os.path.join(os.environ['TEMP'])
    path=zip_item(BDPATH,SRC)
    SRC = os.path.join(os.environ['TEMP'],'mailjet')
    from distutils.dir_util import copy_tree
    copy_tree(SRC, DEST)
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
    DEST=Import_pubnub(DEST)

if 'PROGRAMW6432' in os.environ.keys():
    log_folders=[r"C:\Program Files (x86)\COMODO\Comodo ITSM\cpmlogs",r"C:\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs"]
else:
    log_folders=[r"C:\Program Files\COMODO\Comodo ITSM\cpmlogs",r"C:\Program Files\COMODO\Comodo ITSM\rmmlogs"]
Dest_path = os.path.join(os.environ["PROGRAMDATA"])+r'\CCC'
if os.path.exists(Dest_path):
    Dest_path=Dest_path
else:
    try:
        os.mkdir(Dest_path)
    except:
        pass
for i in range(0,2):
               source_path = log_folders[i]
               copy_tree(source_path, Dest_path)
path_dest=os.path.join(os.environ['PROGRAMDATA'])+r'\\'+os.environ['COMPUTERNAME']+r'.zip'
path_sourc=Dest_path
fantasy_zip = zipfile.ZipFile(path_dest, 'w')
for folder, subfolders, files in os.walk(path_sourc):
    for file in files:
        fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), path_sourc), compress_type = zipfile.ZIP_DEFLATED)
fantasy_zip.close()
fileToSend=path_dest
Email(fileToSend,emailto)
try:
    os.remove(fileToSend)
    shutil.rmtree(Dest_path)
except:
    pass
