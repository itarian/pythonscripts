import ssl
import os
import difflib
from urllib2 import urlopen
import sys
import socket
import json
context = ssl._create_unverified_context()
exip = urlopen('https://api.ipify.org/',context=context).read()
ip=socket.gethostbyname(socket.gethostname())
fileToSend1=os.path.join(os.environ['ProgramData'],'file.txt')
fileToSend2=os.path.join(os.environ['ProgramData'],'file_new.txt')

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))


def write():
    if os.path.exists(fileToSend1):
        with open(fileToSend2, 'w+') as f:
                f.write(exip)
               
    else:
        with open(fileToSend1, 'w+') as f:
                f.write(exip)
                
    if not os.path.exists(fileToSend2):
        with open(fileToSend1, 'w+') as f:
                f.write(exip)
        with open(fileToSend2, 'w+') as f1:
                f1.write(exip)
def compare():
    file1=fileToSend1
    file2=fileToSend2
    c=0
    if False==0:
        with open(file1) as file:
           data=file.read()
           data.strip()
           with open(file2) as file:
               data2=file.read()
               data2.strip()
               text1Lines = data.splitlines(1)
               text2Lines = data2.splitlines(1)
               diffInstance = difflib.Differ()
               diffList = list(diffInstance.compare(text1Lines,text2Lines ))
               for line in diffList:
                   if line.startswith('+') or line.startswith('-'):
                       c=1
                   
           file.close()
        file.close()
    return c

def remove():
    os.remove(fileToSend1)
    os.rename(fileToSend2,fileToSend1)

write()
s=compare()

if s==1:
    alert(1)
    print '\n'
    print 'Changes made External IP,please check the location details below'
    print '\n'
    remove()
    url = 'http://api.db-ip.com/v2/free/{0}'.format(exip)
    response = urlopen(url,context=context)
    data = json.load(response)
    IP=data['ipAddress']
    continentCode=data['continentCode']
    continentName = data['continentName']
    countryCode=data['countryCode']
    countryName=data['countryName']
    state=data['stateProv']
    city=data['city']
    print 'Your location details'
    print '---------------------'
    print 'IP : {0} \ncontinentCode : {1} \ncontinentName : {2} \ncountryCode : {3} \ncountryName : {4} \nstate : {5} \ncity : {6}'.format(IP,continentCode,continentName,countryCode,countryName,state,city)

else:
    print 'No changes in External IP'
    alert(0)
    
