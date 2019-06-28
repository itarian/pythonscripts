CMDLOGON=r'wevtutil qe Security "/q:*[System [(EventID=4648)]]" /rd:true  /f:text> "C:\ProgramData\logon.txt"'
CMDLOGOFF=r'wevtutil qe Security "/q:*[System [(EventID=4647)]]" /rd:true   /f:text> "C:\ProgramData\logoff.txt"'
import ctypes
import re
import subprocess
import os
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
def command(CMD):
    with disable_file_system_redirection():
        process=subprocess.Popen(CMD,shell=True,stdout=subprocess.PIPE);
        result=process.communicate()[0]
        ki=(result)
        
command(CMDLOGON)
command(CMDLOGOFF)
with open(r"C:\ProgramData\logon.txt") as f:
    ki=f.read()
    date=re.findall("Date:(.*)",ki)
    user=re.findall("Account Whose Credentials Were Used:\n(.*)\n(.*)",ki)
login=[]
with open(r"C:\ProgramData\logonlogs.txt","w")as f2:
    for x,y in zip(date,user):
        ki="Login time"+x+y[0]+y[1]
        f2.write(ki)
        f2.write("\n")
with open(r"C:\ProgramData\logoff.txt") as f:
    ki=f.read()
    date=re.findall("Date:(.*)",ki)
    user=re.findall("\n(.*)Account Name:(.*)\n(.*)",ki)
with open(r"C:\ProgramData\logofflogs.txt","w")as f2:
    for x,y in zip(date,user):
        ki=r"Logoff time"+x+"  Account Name:"+y[1]+y[2]
        f2.write(ki)
        f2.write("\n")
if os.path.exists(r"C:\ProgramData\logofflogs.txt"):
    print "Log off logs is successfully generated"
    print "Check your logs at this location"
    print "C:\ProgramData\logofflogs.txt"
else:
    print "Error generating the logs"
if os.path.exists(r"C:\ProgramData\logonlogs.txt"):
    print "Log on logs is successfully generated"
    print "Check your logs at this location"
    print r"C:\ProgramData\logonlogs.txt"
else:
    print "Error generating the logs"
