TASKNAME=r"" #specify your exact task name between the double quotes
ps_command=r'SCHTASKS /Query /TN "'+TASKNAME+'" /FO list /v'
import subprocess
import ctypes
import re
import sys
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
info="""
0 - The operation completed successfully.
1 - Incorrect function called or unknown function called. 2 File not found.
10 - The environment is incorrect. 
267008 - Task is ready to run at its next scheduled time. 
267009 - Task is currently running. 
267010 - The task will not run at the scheduled times because it has been disabled. 
267011 - Task has not yet run. 
267012 - There are no more runs scheduled for this task. 
267013 - One or more of the properties that are needed to run this task on a schedule have not been set. 
267014 - The last run of the task was terminated by the user. 
267015 - Either the task has no triggers or the existing triggers are disabled or not set. 
2147750671 - Credentials became corrupted. 
2147750687 - An instance of this task is already running. 
2147943645 - The service is not available (is "Run only when an user is logged on" checked?). 
3221225786 - The application terminated as a result of a CTRL+C. 
3228369022 - Unknown software exception.
"""
def extractMax(input): 
     numbers = re.findall('\d+',input)
     if numbers:
         return numbers[0]
     else:
         return "Error excuting script"
         
        
def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))

def output(result,info):
    z = re.findall("Last Result:(.*)",result)
    if z:
        spc=z[0].replace(" ","")
        if int(spc) == 1 or int(spc)==10 or int(spc)==267013 or int(spc)==267014 or int(spc)==267015 or int(spc)==2147750671 or  int(spc)==3228369022 or int(spc)==214794364:
            for i in info.splitlines():
                num=extractMax(i)
                spc=spc.replace("\r","")
                if str(num) == str(spc):
                    print "Task scheduler error:"+i
                    alert(1)
            
        else:
            for i in info.splitlines():
                num=extractMax(i)
                spc=spc.replace("\r","")
                if str(num) == str(spc):
                    print "Task scheduler success:"+i
                    alert(0)
                


with disable_file_system_redirection():
    process=subprocess.Popen(ps_command, shell=True, stdout=subprocess.PIPE)
result=process.communicate()
ret=process.returncode
if ret==0:
    output(result[0],info)
else:
    print "Error excuting the script"
    alert(0)
