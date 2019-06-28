User='Sakara' #Provide your user name for cobian backup 
Password = 'Universe' # Provide your password for cobian backup 

import ssl
import os
import urllib2
import subprocess
import codecs
import hashlib
import shutil
ssl._create_default_https_context = ssl._create_unverified_context
temp_path=os.environ['PROGRAMDATA']+r'\c1_temp'


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


sha_signature = encrypt_string(Password)

if 'PROGRAMW6432' in os.environ.keys():
    Installation_directory='C:\Program Files (x86)\Cobian Backup 11'
    

else:
    Installation_directory='C:\Program Files\Cobian Backup 11'


fil='''Cobian Backup 11 Gravity
License accepted=true
Installation directory=%s
Create start menu icons=true
Install VSC=true
Installation type=0
Service account=1
User name=%s
Password=%s
Autostart UI=true
'''%(Installation_directory,User,sha_signature)

if not os.path.exists(temp_path):
    os.makedirs(temp_path)

if 'PROGRAMW6432' in os.environ.keys():
    path_check='C:\Program Files (x86)\Cobian Backup 11'

else:
    path_check='C:\Program Files\Cobian Backup 11'

url=r'http://files.cobiansoft.com/programz/cbSetup.exe'
temp_path=os.environ['PROGRAMDATA']+r'\c1_temp'
setup_file="cbSetup.txt"
setup_exe='cbSetup.exe'
config_path=temp_path+'\\'+setup_file

with codecs.open(config_path, 'w+' , 'utf-16-le') as f:
    f.write(fil)

if os.path.exists(path_check):
    print "Cobian Backup Already installed in your machine..."

else:
    def Download(temp_path,url):
        fileName = 'cbSetup.exe'
        fp = os.path.join(temp_path, fileName)
        request = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        parsed = urllib2.urlopen(request)
        if os.path.exists(temp_path):
            pass
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        with open(fp, 'wb') as f:
            while True:
                chunk=parsed.read(100*1000*1000)
                if chunk:
                    f.write(chunk)
                else:
                    break

        return fp

    Download(temp_path,url)

    def executems():
        os.chdir(temp_path)  
        cmd1=(setup_exe + ' ini=%s' %setup_file)
        ping = subprocess.Popen(cmd1,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out=ping.communicate()[0]
        output = str(out)
        print output
        print "Cobian Backup 11 Successfully installed in your system"

    executems()
    
try:
    shutil.rmtree(temp_path)

except:
    pass
