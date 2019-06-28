from ftplib import FTP
import sys
import os

SERVER = r'CHANGE ME'             #Provide Your FTP Server Address
USER = r'CHANGE ME'               #Provide Your FTP Server User Name
PASS = r'CHANGE ME'               #Provide Your FTP Server Password
PORT = CHANGE ME                  #Provide Your FTP Server PORT Number
FILE_Path = r"C:\Program Files (x86)\AutoIt3\Au3Check.exe"  #Provide the Path of the File or Folder to be Copied. 
def connect_ftp():
    #Connect to the server
    ftp = FTP()
    ftp.connect(SERVER,PORT)
    ftp.login(USER, PASS)
    return ftp

def upload1(path):
    f=path
    os.path.isfile(path + r'\{}'.format(f))
    fh = open(f, 'rb')
    ftp_conn.storbinary('STOR '+ os.path.basename(f), fh)
    fh.close()
def upload(path):
    files = os.listdir(path)
    os.chdir(path)
    for f in files:
        if os.path.isfile(path + r'\{}'.format(f)):
            fh = open(f, 'rb')
            ftp_conn.storbinary('STOR %s' % f, fh)
            fh.close()
        elif os.path.isdir(path + r'\{}'.format(f)):
            ftp_conn.mkd(f)
            ftp_conn.cwd(f)
            upload(path + r'\{}'.format(f))
    ftp_conn.cwd('..')
    os.chdir('..')
ftp_conn = connect_ftp()
if os.path.isfile(FILE_Path):
    upload1(FILE_Path)
else:
    f=os.path.basename(FILE_Path)
    ftp_conn.mkd(f)
    ftp_conn.cwd(f)
    upload(FILE_Path)
print "Files Uploaded to FTP Succesfully"

