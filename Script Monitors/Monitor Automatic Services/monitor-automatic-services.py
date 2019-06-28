import os 
import sys
import ctypes

ale=0
def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))
   
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

with disable_file_system_redirection():
    x=os.popen("wmic service where startmode='Auto' get name").read()
    service_List =[i.strip() for i in x.split('\n') if i.strip() if i.strip() != 'Name']
    for i in service_List:
        y=os.popen("wmic service %s get state"%i).read()
        state_List =[j.strip() for j in y.split('\n') if j.strip() if j.strip() != 'State']
        for j in state_List:
            if "Running" not in j:
                ale=ale+1
                print i+' service in '+ j+' state'
if ale>=1:
    alert(1)
else:
    print "All automatic services are in Running State"
    alert(0)
               

