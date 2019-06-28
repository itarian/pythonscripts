import os
import urllib
import subprocess 


global temp
temp=os.environ['TEMP']
url='http://static.auslogics.com/en/disk-defrag/disk-defrag-setup.exe'

def downloadFile(DownTo, fromURL):
    try:
        fileName = fromURL.split('/')[-1]
        DownTo = os.path.join(DownTo, fileName)        
        with open(DownTo, 'wb') as f:
            f.write(urllib.urlopen(fromURL).read())
        if os.path.isfile(DownTo):
            return '{} - {}KB'.format(DownTo, os.path.getsize(DownTo)/1000)
    except:
        return 'Please Check URL or Download Path!'

def install():
    import subprocess
    sp = subprocess.Popen(temp+r'\disk-defrag-setup.exe  /SP- /SUPPRESSMSGBOXES /VERYSILENT', stdout=subprocess.PIPE)
    out,err = sp.communicate()
    rc = sp.returncode
    if rc==0:
        print out
        print 'Auslogics defragmentation has been installed successfully '
    else:
        print err
    return()


def  run(path):
    os.chdir(path)
    code={0:'Success',1:'Error defragmenting one or more disks.',2:'Administrator access rights are required to defragment disks.',3:'The command line parameters are invalid.',4:'Defragmentation was cancelled by user.',5:'Unsupported Windows version.',6:'Error creating log file.',7:'Another instance is already running.',8:'Low free space on the disk.',9:'The computer has been turned off or rebooted.'}
    defrag = subprocess.Popen('cdefrag.exe -c -f', stdout=subprocess.PIPE)
    out,err = defrag.communicate()
    rc = defrag.returncode
    if rc==0:
        print out
        print 'Auslogics  completed defragmentation process '
    else:
        print err
        print code[rc]    
    os.chdir(temp)
    return()

def uninstall(path):
    os.chdir(path)
    remove= subprocess.Popen('unins000.exe /VERYSILENT /SUPPRESSMSGBOXES', stdout=subprocess.PIPE)
    out,err = remove.communicate()
    rc = remove.returncode
    if rc==0:
        print out
        print 'Auslogics defragmentation has been uninstalled successfully '
    else:
        print err
        print 'Auslogics defragmentation  uninstallation has been failed'
    os.chdir(temp)
    return()


print downloadFile(temp,url)

if 'PROGRAMW6432' in os.environ.keys():
        command_path=r'C:\Program Files (x86)\Auslogics\Disk Defrag'
        uninstall_path= r'C:\Program Files (x86)\Auslogics\Disk Defrag'
else:
        command_path='C:\Program Files\Auslogics\Disk Defrag'
        uninstall_path=r'C:\Program Files\Auslogics\Disk Defrag'



install()
run(command_path)
uninstall(uninstall_path)
os.chdir(temp)
os.remove('disk-defrag-setup.exe')
