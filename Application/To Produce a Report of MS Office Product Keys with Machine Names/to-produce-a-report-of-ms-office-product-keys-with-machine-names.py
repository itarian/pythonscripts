key="XXXXX-XXXXX-XXXXX-XXXXX-XXXXX"  # Give your new Product key which is valuable.
save_path="C:\ProgramData"
file_name="MS_Report.txt"


file_path=save_path+'\\'+file_name
def start(key,save_path,file_name,file_path):
    import os
    import ctypes
    import sys
    import platform
    import subprocess
    import ctypes
    import re
    import shutil

    file_path=save_path+'\\'+file_name
    if os.path.exists(file_path):
        os.remove(file_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    n=[]    
    f='\ospp.vbs'
    cmd1=' /dstatus'
    cmd2=' /unpkey:'
    cmd3=' /inpkey:'
    cmd4=' /act'

    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)

    def os_bits():
        y=platform.machine()
        if y=='AMD64':
            return 64
        else:
            return 32
    def get_version(c):
        with disable_file_system_redirection():
            os.chdir(c)
            a=os.popen('Dir').read()
            b=re.findall('Office(.*)' ,a)
            d='office'+b[1]
        return d
    def run_cmd1():
        with disable_file_system_redirection():
            i=os.popen('cscript '+'"'+c+'"'+cmd1+' > '+file_path).read()

    def run_cmd2(w):
        with disable_file_system_redirection():
          with open(w,'r') as r:
              for line in r.readlines():
                  if line:
                      line=line.strip()
                      if  line.startswith('Last'):
                          s=line
                          j=s.split('key')
                          k=s.split(':',)
                          x=k[1].strip()      
                          i=os.popen('cscript '+'"'+c+'"'+cmd2+x+' >> '+file_path).read()
                  else:
                     pass

    def run_cmd3():
        with disable_file_system_redirection():
            i=os.popen('cscript '+'"'+c+'"'+cmd3+key+' >> '+file_path).read()
    def run_cmd4():
        with disable_file_system_redirection():
            i=os.popen('cscript '+'"'+c+'"'+cmd4+' >> '+file_path).read()


    x=os_bits()
    if x == 64:
        c="C:\Program Files (x86)\Microsoft Office"

    else:
        c="C:\Program Files\Microsoft Office"  


    y=get_version(c)
    c=c+'\\'+y+f
    w=file_path
    run_cmd1()
    run_cmd2(w)
    run_cmd3()
    run_cmd4()
    print "Output file has created in the specified path:\n"
    print file_path




import os
import ctypes


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
def check():

    with disable_file_system_redirection():
        inst=os.popen("wmic product get name,identifyingnumber").read()


    return inst


inst=check()

if 'Microsoft Office' in inst:
    print "Microsoft Office is installed in the Endponit\n"
    print "Activation process has Started\n"
    start(key,save_path,file_name,file_path)
else:
    print "Microsoft Office is not installed in the Endpoint"
