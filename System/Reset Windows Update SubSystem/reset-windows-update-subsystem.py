BAT='''

regsvr32.exe /s atl.dll
regsvr32.exe /s urlmon.dll
regsvr32.exe /s mshtml.dll
regsvr32.exe /s shdocvw.dll
regsvr32.exe /s browseui.dll
regsvr32.exe /s jscript.dll
regsvr32.exe /s vbscript.dll
regsvr32.exe /s scrrun.dll
regsvr32.exe /s msxml.dll
regsvr32.exe /s msxml3.dll
regsvr32.exe /s msxml6.dll
regsvr32.exe /s actxprxy.dll
regsvr32.exe /s softpub.dll
regsvr32.exe /s wintrust.dll
regsvr32.exe /s dssenh.dll
regsvr32.exe /s rsaenh.dll
regsvr32.exe /s gpkcsp.dll
regsvr32.exe /s sccbase.dll
regsvr32.exe /s slbcsp.dll
regsvr32.exe /s cryptdlg.dll
regsvr32.exe /s oleaut32.dll
regsvr32.exe /s ole32.dll
regsvr32.exe /s shell32.dll
regsvr32.exe /s initpki.dll
regsvr32.exe /s wuapi.dll
regsvr32.exe /s wuaueng.dll
regsvr32.exe /s wuaueng1.dll
regsvr32.exe /s wucltui.dll
regsvr32.exe /s wups.dll
regsvr32.exe /s wups2.dll
regsvr32.exe /s wuweb.dll
regsvr32.exe /s qmgr.dll
regsvr32.exe /s qmgrprxy.dll
regsvr32.exe /s wucltux.dll
regsvr32.exe /s muweb.dll
regsvr32.exe /s wuwebv.dll

'''
import os
import sys
import platform
import subprocess
import ctypes

os_details = platform.release()


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

path=os.environ['programdata']+"\Sample.bat"
with open(path,"w") as f:
    f.write(BAT)
    
with disable_file_system_redirection():
    Stop_bits=os.popen("net stop bits").read()
    print Stop_bits
    win_stop_update=os.popen("net stop wuauserv").read()
    print win_stop_update
    cmd1=os.popen("net stop appidsvc").read()
    print cmd1
    cmd2=os.popen("net stop cryptsvc").read()
    print cmd2
    path_new=r"C:\ProgramData\Microsoft\Network\Downloader"
    os.chmod(path_new, 0644)
    os.chdir(path_new)
    if "10" in os_details:
        cmd3=os.popen("del qmgr.dll").read()
        print cmd3
    else:
        cmd3=os.popen("del qmgr*").read()
        print cmd3
    print "Excuting Windows Commands"
    process = subprocess.Popen([path],stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    print "---------------------------"
    print stdout
    cmd4=os.popen("netsh winsock reset").read()
    print cmd4
    cmd5=os.popen("netsh winhttp reset proxy").read()
    print cmd5
    Start_bits=os.popen("net start bits").read()
    print Start_bits
    win_start_update=os.popen("net start wuauserv").read()
    print win_start_update
    cmd6=os.popen("net start appidsvc").read()
    print cmd6
    cmd7=os.popen("net start cryptsvc").read()
    print cmd7
    
    

print "System will restart for applying changes in endpoint"
print "Restart begins...."
rstrt=os.popen("shutdown -r").read()
print rstrt

if os.path.exists(path):
    try:
        os.remove(path)
        print "File removed from your system"
    except:
        pass

else:
    print "File Doesnt exist"
