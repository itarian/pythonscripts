#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name

user_names=itsm.getParameter('User_Names') # List
apikey=itsm.getParameter('Api_Key') # String
domain=itsm.getParameter('Domain_Name') # String
email=itsm.getParameter('From_Email') # String


import os
import ctypes
import subprocess
from subprocess import PIPE, Popen
import sys
flag=0


def sd():
    import requests,json,ast
    payload='''{
            "email": "%s",
            "summary": "Disable User",
            "description": "Succesfully disabled the User(s)",
            "assetType": "2",
            "helpTopic": "1",
            "ticketCategory": "17",
            "category": "1"
            }'''%(email)


    url = "%s/clientapi/index.php?serviceName=createticket"%domain


    headers = {
    "Content-Type" : "application/json",
    "Authorization" : "%s"%(apikey)
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    ret=response.status_code
    if ret==200:
        result=response.json()
        if str(result['status'])=="SUCCESS":
            print "Ticket created Successfully on the service desk"
            k1=str(result['data'])
            k2=result['message']
            print '\t*)',k1.replace('u','').replace(':','').replace('}','').replace('{','').replace("'",'')
            print '\t*)',k2
        else:
            print "Error on the ticket creation on the service "


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
def zip_item(path,final_path):  # Creating ZIP file
    import zipfile
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(final_path)
    zip_ref.close()
    return final_path
def Import_request(DEST):
    BDPATH = Download(r'https://drive.google.com/uc?export=download&id=1utNFdq-PE8viojsFryrjUYX4bzvNSbW5', FileName = 'requests.zip')
    SRC = os.path.join(os.environ['TEMP'])
    path=zip_item(BDPATH,SRC)
    SRC = os.path.join(os.environ['TEMP'],'requests')
    from distutils.dir_util import copy_tree
    copy_tree(SRC, DEST)
    print "REQUEST IMPORTED SUCCESSFULLY"
import os,platform
arch=platform.machine()
if arch=='x86':
    HOMEPATH =r"C:\Program Files"
else:
    HOMEPATH = r"C:\Program Files (x86)"
    
DEST= os.path.join(HOMEPATH,r'COMODO\Comodo ITSM\Lib\site-packages')
Folders=os.listdir(DEST)
Nodow=0
Del_folders=['certifi', 'certifi-2018.10.15.dist-info','chardet', 'chardet-3.0.4.dist-info','requests','requests-2.20.1.dist-info','urllib3','urllib3-1.24.1.dist-info','idna-2.7.dist-info']
for i in Del_folders:
    if i in Folders:
        Nodow=Nodow+1

    
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
for i in user_names:
    with disable_file_system_redirection():
        obj = subprocess.Popen('net user %s  /active:no' %(i), shell = True, stdout = PIPE, stderr = PIPE)
        out, err = obj.communicate()
        if out:
            print "Username : "+i+" sucessfully disabled"
            flag=flag+1
        else:
            if "The user name could not be found" in err:
                print "Username : "+i+" cannot be found"
            else:
                print "Failed Username: "+i
                print err
    
if flag!=0:
    if Nodow>7:
        print "REQUEST AlREADY EXISTS"
        sd()
    else:
        DEST=Import_request(DEST)
        sd()
#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name

user_names=itsm.getParameter('User_Names') # List
apikey=itsm.getParameter('Api_Key') # String
domain=itsm.getParameter('Domain_Name') # String
email=itsm.getParameter('From_Email') # String


import os
import ctypes
import subprocess
from subprocess import PIPE, Popen
import sys
flag=0


def sd():
    import requests,json,ast
    payload='''{
            "email": "%s",
            "summary": "Disable User",
            "description": "Succesfully disabled the User(s)",
            "assetType": "2",
            "helpTopic": "1",
            "ticketCategory": "17",
            "category": "1"
            }'''%(email)


    url = "%s/clientapi/index.php?serviceName=createticket"%domain


    headers = {
    "Content-Type" : "application/json",
    "Authorization" : "%s"%(apikey)
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    ret=response.status_code
    if ret==200:
        result=response.json()
        if str(result['status'])=="SUCCESS":
            print "Ticket created Successfully on the service desk"
            k1=str(result['data'])
            k2=result['message']
            print '\t*)',k1.replace('u','').replace(':','').replace('}','').replace('{','').replace("'",'')
            print '\t*)',k2
        else:
            print "Error on the ticket creation on the service "


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
def zip_item(path,final_path):  # Creating ZIP file
    import zipfile
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(final_path)
    zip_ref.close()
    return final_path
def Import_request(DEST):
    BDPATH = Download(r'https://drive.google.com/uc?export=download&id=1utNFdq-PE8viojsFryrjUYX4bzvNSbW5', FileName = 'requests.zip')
    SRC = os.path.join(os.environ['TEMP'])
    path=zip_item(BDPATH,SRC)
    SRC = os.path.join(os.environ['TEMP'],'requests')
    from distutils.dir_util import copy_tree
    copy_tree(SRC, DEST)
    print "REQUEST IMPORTED SUCCESSFULLY"
import os,platform
arch=platform.machine()
if arch=='x86':
    HOMEPATH =r"C:\Program Files"
else:
    HOMEPATH = r"C:\Program Files (x86)"
    
DEST= os.path.join(HOMEPATH,r'COMODO\Comodo ITSM\Lib\site-packages')
Folders=os.listdir(DEST)
Nodow=0
Del_folders=['certifi', 'certifi-2018.10.15.dist-info','chardet', 'chardet-3.0.4.dist-info','requests','requests-2.20.1.dist-info','urllib3','urllib3-1.24.1.dist-info','idna-2.7.dist-info']
for i in Del_folders:
    if i in Folders:
        Nodow=Nodow+1

    
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
for i in user_names:
    with disable_file_system_redirection():
        obj = subprocess.Popen('net user %s  /active:no' %(i), shell = True, stdout = PIPE, stderr = PIPE)
        out, err = obj.communicate()
        if out:
            print "Username : "+i+" sucessfully disabled"
            flag=flag+1
        else:
            if "The user name could not be found" in err:
                print "Username : "+i+" cannot be found"
            else:
                print "Failed Username: "+i
                print err
    
if flag!=0:
    if Nodow>7:
        print "REQUEST AlREADY EXISTS"
        sd()
    else:
        DEST=Import_request(DEST)
        sd()
