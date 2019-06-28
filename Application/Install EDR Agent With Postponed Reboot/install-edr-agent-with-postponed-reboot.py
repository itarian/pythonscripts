#
### PARAMETERS TO BE EDITED UNDER PARAMETERS TAB ###
#
#1.Enter_the_URL:
# TYPE: String
# ITSM LABEL: Any name
# Default value: "Enter your URL"
#
#2.Enter_the_filename
# TYPE: String
# ITSM LABEL: Any name
# Default value: "Enter your filename"
#
#3.Enter the Extension
# TYPE: String
# ITSM LABEL: Any name
# Default value: "Enter the Extension". For Eg: .exe
#
## Please download COMODO EDR agent (.EXE) file and Upload it in your Host Environment Drive.

URL=itsm.getParameter('Enter_the_URL') # Enter the URL
FileName=itsm.getParameter('Enter_the_filename') # Give your FileName as it is in Drive and ensure downloaded filename and Uploaded filename has not changed.
Extension=itsm.getParameter('Enter_the_extension') # ENter the extension. For Eg: ".exe"
import urllib


fn = FileName+Extension
a = 0
import os
import ctypes
import subprocess
import shutil,time
import ssl
import re
import time
import sys
try:
    import urllib.request as urllib2
except ImportError:
    try:
        import urllib2
    except ImportError:
        pass


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


context = ssl._create_unverified_context()   

def check():
    with disable_file_system_redirection():
        inst=os.popen("wmic product get name,identifyingnumber").read()
    return inst
        
def Download(URL,fileName):
    import os
    print ("Download has started.")
    src_path=os.environ['ProgramData']
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if not os.path.exists(src_path):
        os.makedirs(src_path)
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    print ("The file was successfully downloaded in the specified path: "+fp+".")
    try:
        print('Installation started for Application %s '%fileName)
        dr=os.popen(fp+' /quiet').read()
        print (dr)
    except:
        print ('File: '+fp+' does not exist.')

inst=check()
if len(inst)>0:
	find=re.findall('{.*}\s\sCOMODO\scWatch\sEDR\sAgent',inst)
	if len(find)>0:
		final=re.findall('{.*}',find[0])[0]
		if len(final) >0:
			a=1
if a ==1:
    print ("COMODO cWatch EDR Agent  is installed on the Endpoint. No action required.")
else:
    print ("COMODO cWatch EDR Agent is not installed on the Endpoint.")
    Download(URL,fn)
    a=0
    inst=check()
    if len(inst)>0:
        find=re.findall('{.*}\s\sCOMODO\scWatch\sEDR\sAgent',inst)
        if len(find)>0:
            final=re.findall('{.*}',find[0])[0]
            if len(final) >0:
                a=1
    if a ==1:
        print ("COMODO cWatch EDR Agent  is installed on the Endpoint.")
    else:
        print ("COMODO cWatch EDR Agent is not installed on the Endpoint.")
