#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name

import os
import shutil
import zipfile
import _winreg
import random
import string
import ctypes

def downloadFile(DownTo, fromURL, Ext=None):
    import urllib2
    try:
        fileName = fromURL.split('/')[-1]
        if Ext:
            DownTo = os.path.join(DownTo, fileName+Ext)
        else:
            DownTo = os.path.join(DownTo, fileName)
        with open(DownTo, 'wb') as f:
            f.write(urllib2.urlopen(fromURL).read())
        if os.path.isfile(DownTo):
            return (DownTo, os.path.getsize(DownTo)/1000)
    except:
        return 'Please Check %s or %s'%(fromURL, DownTo)


class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
                
def filezip(src_path,dest_path):
	with disable_file_system_redirection():
		with zipfile.ZipFile(src_path,"r") as zip_ref:
			zip_ref.extractall(dest_path)
			print 'file successfully unzipped'

def Download(path, URL):
    import urllib2
    import os
    print "Download started"
    fileName ="ccsetup557.zip"
    fp = os.path.join(path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(path):
        print "Path already exists"
    if not os.path.exists(path):
        os.makedirs(path)
        print "Path created"
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    print "The file downloaded successfully in specified path"
    return fp

def ecmd(CMD, r=False):  
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    ret=OBJ.returncode
    if r:
        return ret
    else:            
        if ret==0:
            return out
        else:
            return ret

def deleteall(path):
    import shutil
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            f=os.path.join(root,name)
            try:
                os.remove(f)
            except:
                pass
        for name in dirs:
            p=os.path.join(root,name)
            try:
                shutil.rmtree(p)
            except:
                pass
    return '%s %s Cleared'%(path, str(20*'.'))

osdrive=os.environ['SYSTEMDRIVE']
i=0
fnlist=''
while True:
    tmp=str(random.randint(0,10))+random.choice(list(string.ascii_lowercase))
    fnlist+=tmp
    if i==3:
        break
    i+=1
os_temp=os.path.join(osdrive, os.sep, fnlist)
ecmd('mkdir %s'%(os_temp))
##--------------------------------------------------
print '.. Clears all Windows Temp Files ..'
print deleteall(os.environ['TEMP'])
rootpath=os.path.join(osdrive, os.sep, 'Users')
for namedirs in os.listdir(rootpath):
    if os.path.isdir(os.path.join(rootpath, namedirs)):
        temp_path=os.path.join(rootpath, namedirs, 'AppData', 'Local', 'Temp')
        if os.path.isdir(temp_path):
            print deleteall(temp_path)
##--------------------------------------------------
print '\n.. Clears all Internet Temp Files ..'
kill_firefox='taskkill /f /im firefox.exe'
kill_chrome='taskkill /f /im chrome.exe'
kill_ie='taskkill /f /im iexplore.exe'
try:
    ecmd(kill_firefox)
    ecmd(kill_chrome)
    ecmd(kill_ie)
except:
    pass
for namedirs in os.listdir(rootpath):
    if os.path.isdir(os.path.join(rootpath, namedirs)):
        chrome_path=os.path.join(rootpath, namedirs, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cache')
        if os.path.isdir(chrome_path):
            print deleteall(chrome_path)
        firefox_path=os.path.join(rootpath, namedirs, 'AppData', 'Local', 'Mozilla', 'Firefox', 'Profiles')
        if os.path.isdir(firefox_path):
            print deleteall(firefox_path)
ie_cache="RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 8 "
ie=ecmd(ie_cache, True)
if ie==0:
    print 'IE Cache %s Cleared'%(20*'.')
else:
    print '%s %d Error on IE Cache'%(20*'.', ie)
##--------------------------------------------------
print '\n.. Disk Cleaning ..'
dc=ecmd('cleanmgr /sagerun:64', True)
if dc==0:
    print 'Disk %s Cleaned-up'%(20*'.')
else:
    print '%s %d Error on Disk Cleans-up'%(20*'.', dc)

curl='https://onedrive.live.com/download?cid=A910C8EF113350FB&resid=A910C8EF113350FB%21127&authkey=AKhn0M1QkTgfhX0'
fs = Download(os_temp, curl)
#print "fs:"+fs
try:
    ep=os.path.join(os_temp, fs.split(os.sep)[-1][:-4])
    #print "ep:"+ ep
    filezip(fs,ep)
    #print os_temp
    if 'PROGRAMW6432' in os.environ.keys():
        pp=os.path.join(ep, 'CCleaner64.exe')
    else:
        pp=os.path.join(ep, 'CCleaner.exe')
    cc=ecmd('"%s" /auto'%pp, True)
    if cc==0:
        print 'System %s Cleaned-up'%(20*'.')
    else:
        print '%s %d Error on System Cleans-up'%(20*'.', cc)
    shutil.rmtree(ep)
except Exception as e:
    print e

##--------------------------------------------------
print '\n.. Defragmenting ..'
url='http://static.auslogics.com/en/disk-defrag/disk-defrag-setup.exe'
ps=downloadFile(os_temp, url)
if type(ps) is tuple:
    p,s=downloadFile(os_temp, url)
else:
    print ps
if ecmd('"%s" /SP- /SUPPRESSMSGBOXES /VERYSILENT'%p, True)==0:
    ecmd('taskkill /f /im DiskDefrag.exe')
    if 'PROGRAMW6432' in os.environ.keys():
        command_path=os.path.join(os.environ['PROGRAMFILES(X86)'], 'Auslogics', 'Disk Defrag', 'cdefrag.exe')
        uninstall_path=os.path.join(os.environ['PROGRAMFILES(X86)'], 'Auslogics', 'Disk Defrag', 'unins000.exe')
    else:
        command_path=os.path.join(os.environ['PROGRAMFILES'], 'Auslogics', 'Disk Defrag', 'cdefrag.exe')
        uninstall_path=os.path.join(os.environ['PROGRAMFILES'], 'Auslogics', 'Disk Defrag', 'unins000.exe')
    code={0:'Success', 1:'Error defragmenting one or more disks.', 2:'Administrator access rights are required to defragment disks.', 3:'The command line parameters are invalid.', 4:'Defragmentation was cancelled by user.', 5:'Unsupported Windows version.', 6:'Error creating log file.', 7:'Another instance is already running.', 8:'Low free space on the disk.', 9:'The computer has been turned off or rebooted.'}
    print 'Defragmenting %s %s'%(20*'.', code[ecmd('"%s" -c -f'%command_path, True)])
    ecmd('"%s" /VERYSILENT /SUPPRESSMSGBOXES'%uninstall_path)
    pp=os.sep.join(command_path.split(os.sep)[:3])
    if os.path.isdir(pp):
        try:
            shutil.rmtree(pp)
        except:
            pass
    os.remove(p)

##--------------------------------------------------
print '\n.. Fixing Disk Errors (All Unremovable Disks) ..'
dl=ecmd('wmic logicaldisk where drivetype=3 get name')
dls=[i.strip() for i in dl.split('\n') if i.strip()][1:]
df=ecmd('for %%i in (%s) do echo y | chkdsk %%i /f'%(' '.join(dls)), True)
if df==0 or df==3:
    for i in dls:
        if i==os.getenv('SYSTEMDRIVE'):
            print 'Disk Error Fixing %s Will Start on Booting the Computer for %s (OS Drive)'%(20*'.', i)
        else:
            print 'Disk Error Fixing %s Completed for %s'%(20*'.', i)
else:
    print '%s %d Error on Fixing Disk Errors'%(20*'.', df)
##--------------------------------------------------
print '\n.. Clear Printer Spool (Queuing Printer Jobs) ..'
sp=ecmd('net stop spooler', True)
if sp==0:
    cl=ecmd('del %systemroot%\System32\spool\printers\* /Q', True)
    if cl==0:
        print 'Printer Spool %s Cleared'%(20*'.')
    else:
        print '%s %d Error on Printer Spool Cleaning'%(20*'.', cl)
    ecmd('net start spooler')
##--------------------------------------------------
df=ecmd('ipconfig /flushdns', True)
if df==0:
    print '\nDNS Cache %s Cleared'%(20*'.')
else:
    print '\n%s %d Error on DNS Cache Clearing'%(20*'.', df)
ir=ecmd('ipconfig /release', True)
if ir==0:
    print 'IP %s Released'%(20*'.')
else:
    print '%s %d Error on IP Release'%(20*'.', ir)
ire=ecmd('ipconfig /renew', True)
if ire==0:
    print 'IP %s Renewed'%(20*'.')
else:
    print '%s %d Error on IP Renew'%(20*'.', ire)
rc=ecmd('rd /s /q %systemdrive%\$Recycle.bin', True)
if rc==0:
    print 'Recycle Bin %s Cleared'%(20*'.')
##--------------------------------------------------


keyVal = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore'
if 'PROGRAMFILES(X86)' in os.environ.keys():
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,keyVal, 0, _winreg.KEY_WOW64_64KEY|_winreg.KEY_ALL_ACCESS)
else:
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,keyVal, 0, _winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(key, "SystemRestorePointCreationFrequency", 0,_winreg.REG_DWORD,0)


if ecmd('WMIC /Namespace:\\root\default Path SystemRestore Call CreateRestorePoint "BY COMODO ITSM %DATE% %TIME%", 100, 12', True)==0:
    print ecmd('POWERSHELL Get-ComputerRestorePoint')
_winreg.DeleteValue(key, 'SystemRestorePointCreationFrequency')
_winreg.CloseKey(key)
print '\n.. Smart Check for all Disk Drives ..'
print ecmd('wmic diskdrive get status')
shutil.rmtree(os_temp)

