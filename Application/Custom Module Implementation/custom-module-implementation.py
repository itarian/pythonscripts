import os

#################################################
###         Download Hosted Module            ###
#################################################


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


#################################################
###           Zip downloaded Module           ###
#################################################
    
def zip_item(path,final_path):  # Creating ZIP file
    import zipfile
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(final_path)
    zip_ref.close()
    return final_path


#################################################
###           Place zipped Module             ###
#################################################

def Import_module(DEST):
    BDPATH = Download(r'https://drive.google.com/uc?export=download&id=1h3nvQ7hRD68FeRsP5qWjEi1phHAeiL5L', FileName = 'pathlib.zip')
    SRC = os.path.join(os.environ['TEMP'])
    path=zip_item(BDPATH,SRC)
    SRC = os.path.join(os.environ['TEMP'],'pathlib')
    from distutils.dir_util import copy_tree
    copy_tree(SRC, DEST)

    import pathlib
    print "Pathlib is imported"

    
    return DEST

#################################################
### Find 32 or 64 bit & set path for libraries ###
#################################################

HOMEPATH = r"C:\Program Files (x86)"
if os.path.exists(HOMEPATH):
        HOMEPATH = r"C:\Program Files (x86)"
else:
    HOMEPATH =r"C:\Program Files"

DEST= os.path.join(HOMEPATH,r'COMODO\Comodo ITSM\Lib\site-packages')
DEST=Import_module(DEST)


import pathlib
from pathlib import *

# Current windows directory
c=Path.cwd()
print "Current windows directory : "+str(c)+"\n"

# Make it pure windows path
print "Pure Windows path is : "+str(PureWindowsPath('c:/Windows', '/Program Files'))+"\n"


# Retrieve paths per index
p = PureWindowsPath('c:/foo/bar/setup.py')
print "Index[0] : "+str(p.parents[0])
print "Index[1] : "+str(p.parents[1])
print "Index[2] : "+str(p.parents[2])


# join Path
print "\n"+"Joined path is : "+str(PurePosixPath('/etc').joinpath('passwd'))


# Split from first
p = PurePosixPath('/etc/passwd')
print p.relative_to('/')
print p.relative_to('/etc/passwd')

