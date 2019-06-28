import ctypes
import os
pingip=r"CHANGE_ME"  #Provide the domain name or IP address to ping
Send_Email=1         #Provide 1 if you want to send ping status report as an mail or Provide 0 if you don't want to send an mail. 
emailto=r"CHANGE_ME" #Provide the email id for which the report will be sent if you have provided Send_Email as 1                  
fileToSend=os.path.join(os.environ['TEMP'], 'report.txt')
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
                            "Subject": "Ping Status Report",
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
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

command="ping  "+pingip+" >C:\pingstatus.txt"
with disable_file_system_redirection():
    os.popen(command).read()
    average=os.popen('findstr "Average" C:\pingstatus.txt').read()
if average:
    print "ping status of "+pingip+" is "+ average.strip()
    with open(fileToSend, 'w') as f:
        f.write("The ping status for the domain name or ip given by the user  ")
        f.write(pingip)
        f.write("\n")
        f.write(average)
else:
    print "ping status of "+pingip+" is "+" request timed out - failed"
    with open(fileToSend, 'w') as f:
        f.write("The ping status for the domain name or ip given by the user  ")
        f.write(pingip)
        f.write("\n")
        f.write("ping status request is timed out - failed")

HOMEPATH = r"C:\Program Files (x86)"
if os.path.exists(HOMEPATH):
        HOMEPATH = r"C:\Program Files (x86)"
else:
    HOMEPATH =r"C:\Program Files"

DEST= os.path.join(HOMEPATH,r'COMODO\Comodo ITSM\Lib\site-packages')

if Send_Email==1:
    Import_pubnub(DEST)
    Email(fileToSend,emailto)

